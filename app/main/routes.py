from flask import render_template, send_from_directory, request, jsonify
from app.models import Listings, ListingImages
from app.main import bp
from app.logger import *
import datetime
import os

@bp.route('/')
def index():
    listing_ids = []
    top_listings = Listings.get_top_listings(5)
    locations = Listings.get_all_locations(True)
    
    for listing in top_listings:
        listing_ids.append(listing.id)
        
    top_listing_images = ListingImages.get_selected_main_images(listing_ids)
    return render_template(
        'index.html',
        locations=locations,
        top_listings=top_listings, 
        top_listing_images=top_listing_images
    )

@bp.route('/uploads/listing_images/<filename>')
def upload_file(filename):
    try:
        upload_folder = os.path.join(os.getcwd(), 'app/uploads')
        file_directory = send_from_directory(upload_folder, f'listing_images/{filename}')
    except:
        #Fall back for when image is not associated with a booking
        file_directory = send_from_directory(upload_folder, f'listing_images/booking_image_not_found.jpg')
        app_logger.debug(f"Can't find {filename} within uploads folder")
    return file_directory

# Should only be used by ajax calls
@bp.route('/log_message', methods=['POST'])
def log_message():
    try:
        data = request.get_json()
        log_message = data.get('log_message')
        log_type = data.get('type')

        if log_type == 'app':
            app_logger.info(log_message)
        elif log_type == 'db':
            db_logger.info(log_message)
        elif log_type == 'auth':
            auth_logger.info(log_message)
        elif log_type == 'error':
            error_logger.info(log_message)
        elif log_type == 'debug':
            debug_logger.info(log_message)
        else:
            return jsonify({'success': False, 'error': 'Invalid log type'}), 400

        return jsonify({'success': True, 'message': 'Log message recorded'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@bp.route('/about_us')
def about_us():
    return render_template('main/about_us.html')

@bp.route('/faq')
def faq():
    return render_template('main/faq.html')

@bp.route('/privacy_policy')
def privacy_policy():
    return render_template('main/privacy_policy.html')

@bp.route('/tos')
def tos():
    return render_template('main/tos.html')

@bp.route('/contact_us')
def contact_us():
    return render_template('main/contact_us.html')