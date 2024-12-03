from flask import render_template, redirect, url_for
from app.admin import bp
from app.models import Listings, ListingImages 


@bp.route('/manage_listings')
def manage_listings():
    return render_template('admin/index.html', top_listings=top_listings, top_listing_images=top_listing_images)