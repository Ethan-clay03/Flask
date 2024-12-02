from flask import request, jsonify
from app import db

class ListingImages(db.Model):
    __tablename__ = 'listing_images'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    listing_id = db.Column(db.Integer(), nullable=False)
    image_location = db.Column(db.String(255), nullable=False)
    image_description = db.Column(db.String(255), nullable=True)
    main_image = db.Column(db.SmallInteger(), nullable=False)
    listings_id = mapped_column(ForeignKey("listings.id"))
    listings = relationship("Listings", back_populates="listing_images")

    @classmethod
    def get_selected_main_images(cls, listing_ids):
        
        listing_images = cls.query.filter(
            cls.listing_id.in_(listing_ids), 
            cls.main_image == 1 
        ).all()
        
        ordered_listing_images = {listing.listing_id: listing.image_location for listing in listing_images}
        
        return ordered_listing_images