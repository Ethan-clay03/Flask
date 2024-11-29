from flask import render_template, send_from_directory
from app.main import bp
import datetime
import os

@bp.route('/')
def index():
    date=datetime.datetime.now()
    tomorrow_object = date + datetime.timedelta(days=1)
    return render_template('index.html', today = date.strftime('%Y-%m-%d'), tomorrow = tomorrow_object.strftime('%Y-%m-%d'))

@bp.route('/uploads/listing_images/<filename>')
def upload_file(filename):
    
    upload_folder = os.path.join(os.getcwd(), 'app/uploads')
    return send_from_directory(upload_folder, f'listing_images/{filename}')