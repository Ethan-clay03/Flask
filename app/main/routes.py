from flask import render_template, send_from_directory
from app.models import Listings, ListingImages
from app.main import bp
import datetime
import os

@bp.route('/')
def index():
    date=datetime.datetime.now()
    listing_ids = []
    tomorrow_object = date + datetime.timedelta(days=1)
    top_listings = Listings.get_top_listings(5)
    
    for listing in top_listings:
        listing_ids.append(listing.id)
        
    top_listing_images = ListingImages.get_selected_main_images(listing_ids)
    return render_template(
        'index.html', 
        today = date.strftime('%Y-%m-%d'), 
        tomorrow = tomorrow_object.strftime('%Y-%m-%d'),
        top_listings=top_listings, 
        top_listing_images=top_listing_images
    )

@bp.route('/uploads/listing_images/<filename>')
def upload_file(filename):
    
    upload_folder = os.path.join(os.getcwd(), 'app/uploads')
    return send_from_directory(upload_folder, f'listing_images/{filename}')
