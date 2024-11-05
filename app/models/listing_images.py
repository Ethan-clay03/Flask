from flask import request, jsonify
from app import db

class ListingImages(db.Model):
    __tablename__ = 'listing_images'

    id = db.Column(db.Integer(), nullable=False, primary_key=True),
    listing_id = db.Column(db.Integer(), nullable=False),
    image_location = db.Column(db.String(255), nullable=False),
    image_description = db.Column(db.String(255), nullable=True)

    @classmethod
    def get_all_listings(cls):
        pass    