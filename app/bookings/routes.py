from flask import render_template, redirect, url_for
from app.bookings import bp

@bp.route('/home')
def index():
    return render_template('bookings/index.html')

@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.index'), code=301)