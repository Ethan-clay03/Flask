from flask import render_template
from app.bookings import bp

@bp.route('/')
def index():
    return render_template('bookings/index.html')
