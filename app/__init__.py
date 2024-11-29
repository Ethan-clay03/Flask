# Boilerplate create_app code taken from https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Only enabled when DEVELOPMENT_MODE in .env is set to true
    development_mode = os.getenv("DEVELOPMENT_MODE")

    if (development_mode.lower() == 'true'): 
        app.config['DEBUG'] = True

    load_dotenv()
    db_host = os.getenv("DATABASE_HOST")
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_name = os.getenv("DATABASE_NAME")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}".format(db_user=db_user, db_password=db_password, db_name=db_name)
    db.init_app(app)
    
    #Run Flask migrations if any available
    migrate.init_app(app, db)

    # Register blueprints and url prefixes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    if __name__ == "__main__":
        app.run(use_reloader=True)

    return app