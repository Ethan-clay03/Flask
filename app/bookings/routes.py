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
    all_listings = Listings.get_all_listings()
    return render_template('bookings/listings.html', all_listings=all_listings)
