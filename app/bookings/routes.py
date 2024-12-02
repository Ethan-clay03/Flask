from flask import render_template, redirect, url_for
from app.bookings import bp
from app.models import Listings, ListingImages 

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
    return render_template('bookings/listings.html')
