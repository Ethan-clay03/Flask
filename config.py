#TO CHECK IF I CAN MOVE DATABASE CONNECTION HERE OR BETTER IN .env

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BOOKING_IMAGE_UPLOADS = os.path.join(os.getcwd(), 'app/uploads/listing_images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False