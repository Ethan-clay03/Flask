# Boilerplate code taken from https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

from flask import Flask

from config import Config

from flask_cookies import Cookies


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #Cookies, can add optional Google Tag Manager ID below
    cookies = Cookies()
    cookies.init_app(app)
    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')

    @app.route('/test')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app