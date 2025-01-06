from flask import Flask, url_for, redirect, session, g, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_security import Security
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_loaded, identity_changed
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from functools import wraps
import os

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not permission.can():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

from app.models import User, Role, RoleUsers

super_admin_permission = Permission(RoleNeed('super-admin'))
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Only enabled when DEVELOPMENT_MODE in .env is set to true
    development_mode = os.getenv("DEVELOPMENT_MODE")
    if development_mode and development_mode.lower() == 'true':
        app.config['DEBUG'] = True

    load_dotenv()
    db_host = os.getenv("DATABASE_HOST")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_name = os.getenv("DATABASE_NAME")
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

    db.init_app(app)
    migrate.init_app(app, db)

    # Use RoleUsers.get_datastore() instead of RoleUsers.user_datastore
    security = Security(app, RoleUsers.get_datastore())
    principal = Principal(app)

    # Register blueprints and URL prefixes
    register_blueprints(app)

    # Protect internal endpoints from external use
    csrf.init_app(app)

    # Identity loader
    @identity_loaded.connect_via(app)
    # Identity loader
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if current_user.is_authenticated:
            identity.provides.add(RoleNeed('user'))
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
                # Should only be allocated to the root account, used for changing users to user -> admin
                if role.name == 'super-admin':
                    identity.provides.add(RoleNeed('admin'))
                    identity.provides.add(RoleNeed('user'))


    # Add global template variables
    @app.context_processor
    def set_global_html_variable_values():
        try:
            if current_user.is_authenticated:
                user_in_session = True
            else:
                user_in_session = False

            template_config = {
                'user_in_session': user_in_session,
                'admin_permission': g.admin_permission,
                'user_permission': g.user_permission,
                'super_admin_permission': g.super_admin_permission
            }
            return template_config
        except Exception as e:
            return {
                'user_in_session': False,
                'admin_permission': g.admin_permission,
                'user_permission': g.user_permission,
                'super_admin_permission': g.super_admin_permission
            }


    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        session['error_message'] = str(e)
        return redirect(url_for('errors.quandary'))

    @app.before_request
    def before_request():
        g.admin_permission = admin_permission
        g.user_permission = user_permission
        g.super_admin_permission = super_admin_permission
        if current_user.is_authenticated:
            identity_changed.send(current_user._get_current_object(), identity=Identity(current_user.id))


    login_manager.login_view = 'profile.login'
    login_manager.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_blueprints(app):
    blueprints = [
        ('main', None),
        ('bookings', '/bookings'),
        ('api', '/api'),
        ('admin', '/admin'),
        ('profile', '/profile'),
        ('errors', '/errors'),
    ]
    for module_name, url_prefix in blueprints:
        module = __import__(f'app.{module_name}', fromlist=['bp'])
        app.register_blueprint(module.bp, url_prefix=url_prefix)
