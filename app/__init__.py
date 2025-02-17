from flask import Flask, g, abort, current_app, request, session, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed, identity_loaded
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from app.logger import auth_logger, error_logger
from functools import wraps
import os
import pymysql
from sqlalchemy.sql import text

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
principal = Principal()

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not permission.can():
                auth_logger.debug(f'Permission denied for {current_user} attempting to access {request.endpoint}.')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

super_admin_permission = Permission(RoleNeed('super-admin'))
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


def create_database_if_not_exists(db_host, db_user, db_password, db_name):
    try:
        connection = pymysql.connect(
            host=db_host,
            user='root',
            password=db_password
        )
    except:
        error_message = 'Unable to connect to database as the root user, is the docker database running? If issue persists check README.md for help'
        print(error_message)
        error_logger.error(error_message)
        exit()
        

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            # Create the user 
            cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%'")
            cursor.execute(f"FLUSH PRIVILEGES")
        connection.commit()
    finally:
        connection.close()

    # Reconnect using user in .env to prevent permission issues
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Check if tables exist
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            if not tables:
                with open('sql-setup/init.sql', 'r') as file:
                    sql_commands = file.read().split(';')
                    for command in sql_commands:
                        if command.strip():
                            cursor.execute(command)
                connection.commit()
    finally:
        connection.close()



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
    
    create_database_if_not_exists(db_host, db_user, db_password, db_name)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"


    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    principal.init_app(app)

    # Register blueprints and URL prefixes
    register_blueprints(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if current_user.is_authenticated:
            from app.models import User
            identity.provides.add(RoleNeed('user'))
            user = User.query.get(current_user.id)
            if user and user.role:
                identity.provides.add(RoleNeed(user.role.name))
                if user.role.name == 'super-admin':
                    identity.provides.add(RoleNeed('admin'))
            else:
                auth_logger.debug(f'No role found for user {identity.user.username}.')

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

    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     app.logger.error(f"Unhandled exception: {e}")
    #     session['error_message'] = str(e)
    #     return redirect(url_for('errors.quandary'))

    @app.errorhandler(403)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        session['error_message'] = str(e)
        return redirect(url_for('errors.quandary'))

    @app.before_request
    def before_request():
        g.admin_permission = None
        g.user_permission = None
        g.super_admin_permission = None
        g.is_admin = False
        g.is_super_admin = False

        if current_user.is_authenticated:
            role = current_user.role
            if role:
                g.user_permission = user_permission
                if role.name == 'super-admin':
                    g.super_admin_permission = super_admin_permission
                    g.admin_permission = admin_permission
                    g.is_super_admin = True
                    g.is_admin = True
                elif role.name == 'admin':
                    g.admin_permission = admin_permission
                    g.is_admin = True

    login_manager.login_view = 'profile.login' 

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def register_blueprints(app):
    blueprints = [
        ('main', None),
        ('bookings', '/bookings'),
        ('admin', '/admin'),
        ('profile', '/profile'),
        ('errors', '/errors'),
    ]
    for module_name, url_prefix in blueprints:
        module = __import__(f'app.{module_name}', fromlist=['bp'])
        app.register_blueprint(module.bp, url_prefix=url_prefix)
