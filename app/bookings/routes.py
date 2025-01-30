from flask import render_template, redirect, url_for, g
from app.bookings import bp
from app.models import Listings, ListingImages 
import json


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
            item.main_image_url = url_for('main.upload_file', filename='booking_image_not_found.jpg')
        # Must be a single quote JSON otherwise doesn't work in frontend
        item.image_urls = json.dumps([url_for('main.upload_file', filename=img.image_location) for img in item.listing_images]).replace('"', '&quot;')

    return render_template('bookings/listings.html', items=all_listings)




@bp.route('/listing/<int:id>')
def show_listing(id):
    return render_template('bookings/listings.html', id=1)