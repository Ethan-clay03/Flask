from flask import render_template, redirect, url_for, g
from app.bookings import bp
from app.models import Listings, ListingImages 
import json

@bp.route('/home')
def index():
    listing_ids = []
    top_listings = Listings.get_top_listings(5)
    
    for listing in top_listings:
        listing_ids.append(listing.id)
        
    top_listing_images = ListingImages.get_selected_main_images(listing_ids)
    
    return render_template('bookings/index.html', top_listings=top_listings, top_listing_images=top_listing_images)

@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.index'), code=301)


@bp.route('/listings')
def listings():
    all_listings = Listings.get_all_listings()

    for item in all_listings:
        main_image = next((img for img in item.listing_images if img.main_image), None)
        if main_image:
            item.main_image_url = url_for('main.upload_file', filename=main_image.image_location)
        elif item.listing_images:
            item.main_image_url = url_for('main.upload_file', filename=item.listing_images[0].image_location)
        else:
            item.main_image_url = "/path/to/default-image.jpg"
        # Must replace with single quotes otherwise JS does not load modal correctly
        item.image_urls = json.dumps([url_for('main.upload_file', filename=img.image_location) for img in item.listing_images]).replace('"', '&quot;')

    return render_template('bookings/listings.html', items=all_listings)




@bp.route('/listing/<int:id>')
def show_listing(id):
    Listings.get
    return render_template('bookings/listings.html', id=1)