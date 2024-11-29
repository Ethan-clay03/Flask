from flask import render_template, redirect, url_for
from app.bookings import bp
from app.models import Listings 

@bp.route('/home')
def index():
    return render_template('bookings/index.html')

@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.index'), code=301)

@bp.route('/listings')
def listings():
    top_listings = Listings.get_top_listings(5)
    return render_template('bookings/listings.html', top_listings=top_listings)
