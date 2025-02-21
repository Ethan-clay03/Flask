from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db
import os
from app.main.utils import allowed_image_files
from flask import current_app
import uuid

class ListingImages(db.Model):
    __tablename__ = 'listing_images'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    image_location = db.Column(db.String(255), nullable=False)
    main_image = db.Column(db.SmallInteger(), nullable=False)
    listing_id = db.Column(Integer, ForeignKey('listings.id'), nullable=False)
    listing = relationship("Listings", back_populates="listing_images")

    @classmethod
    def get_selected_main_images(cls, listing_ids):
        listing_images = cls.query.filter(
            cls.listing_id.in_(listing_ids),
            cls.main_image == 1
        ).all()

        ordered_listing_images = {listing.listing_id: listing.image_location for listing in listing_images}

        return ordered_listing_images

    @staticmethod
    def save_image(file, listing_id):
        if file and allowed_image_files(file.filename):
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{listing_id}_{uuid.uuid4().hex}.{extension}"  # Unique filename
            upload_folder = current_app.config['BOOKING_IMAGE_UPLOADS']
            file_path = os.path.join(upload_folder, filename)

            try:
                os.makedirs(upload_folder, exist_ok=True)
                file.save(file_path)

                # Create and save new image record
                new_image = ListingImages(
                    listing_id=listing_id,
                    image_location=filename,
                    main_image=False
                )
                db.session.add(new_image)
                db.session.commit()  # Commit here to ensure `id` is generated
                return new_image
            except Exception as e:
                print(f"Error saving file: {e}")
                db.session.rollback()
                return None
        else:
            return False

    @classmethod
    def set_main_image(cls, listing_id, image_id):
        cls.query.filter_by(listing_id=listing_id).update({'main_image': False})
        main_image = cls.query.filter_by(id=image_id, listing_id=listing_id).first()
        if main_image:
            main_image.main_image = True
            db.session.commit()