# Boilerplate create_app code taken from https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #ONLY TURN ON FOR DEBUGGING
    app.config['DEBUG'] = True

    # Database connection , TO DO: Encrypt and move into .env
    db_user = 'ethan2clay'
    db_password = 'Ethan2claY10+$++'
    db_name = 'ethan2clay_prj'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@localhost/{db_name}".format(db_user=db_user, db_password=db_password, db_name=db_name)
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

    return app