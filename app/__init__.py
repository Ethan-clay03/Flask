# Boilerplate create_app code taken from https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

from flask import Flask, url_for, redirect, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Only enabled when DEVELOPMENT_MODE in .env is set to true
    development_mode = os.getenv("DEVELOPMENT_MODE")
    print(development_mode)

    #if (development_mode.lower() == 'true'): 
    app.config['DEBUG'] = True

    load_dotenv()
    db_host = os.getenv("DATABASE_HOST")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_name = os.getenv("DATABASE_NAME")
    
    app.config['SECRET_KEY'] = 'tnm]H+akmfnf_#PT>i|(Qo4LT@+n£9"~e3'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}".format(db_user=db_user, db_password=db_password, db_host=db_host, db_name=db_name)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    
    #Run Flask migrations if any available
    migrate.init_app(app, db)

    # Register blueprints and url prefixes
    register_blueprints(app)

    #Protect internal endpoints from external use
    csrf.init_app(app)
    
    # Add any vars needed accessible through all templates
    @app.context_processor
    def set_global_html_variable_values():
        try:
            if current_user.is_authenticated:
                user_in_session = True
            else:
                user_in_session = False

            template_config = {'user_in_session': user_in_session}
            return template_config
        except Exception as e:
            # print(f"Error in context processor: {e}")
            return {'user_in_session': False}  # Fallback, to create logging to record such failures (database corrupted etc.)
    
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        session['error_message'] = str(e)
        return redirect(url_for('errors.quandary'))
    
    if __name__ == "__main__":
        app.run(use_reloader=True, debug=True)
        
    login_manager.login_view = 'profile.login'
    login_manager.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
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




