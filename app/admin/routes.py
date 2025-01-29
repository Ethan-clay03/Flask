from flask import render_template, redirect, url_for, request, jsonify, flash
from app import db
from app import admin_permission, permission_required, super_admin_permission
from app.models import Listings, ListingImages
from app.admin import bp
from app.main.utils import save_booking_image


@bp.route('/home')
@permission_required(admin_permission)
def index():
    return render_template('admin/index.html')

@bp.route('/')
@permission_required(admin_permission)
def home():
    return redirect(url_for('admin.home'))

@bp.route('/manage_bookings')
@permission_required(admin_permission)
def manage_bookings():
    locations = Listings.get_all_locations()
    return render_template('admin/manage_bookings.html', locations=locations)

@bp.route('/manage_bookings/edit/<int:id>')
@permission_required(admin_permission)
def edit_booking(id):
    locations = Listings.get_all_locations()
    listing_information = Listings.search_listing(id)
    time_options = [
        "00:00", "00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30",
        "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30",
        "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
        "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
        "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"
    ]
    
    # Use the instance of the listing_information object to format the times
    depart_time_str = listing_information.depart_time.strftime("%H:%M")
    destination_time_str = listing_information.destination_time.strftime("%H:%M")
                                                             
    return render_template('admin/edit_booking.html', locations=locations, listing=listing_information, time_options=time_options, depart_time_str=depart_time_str, destination_time_str=destination_time_str)


@bp.route('/manage_users')
@permission_required(super_admin_permission)
def manage_users():
    return render_template('admin/index.html')

@bp.route('/manage_user_bookings')
@permission_required(admin_permission)
def manage_user_bookings():
    return render_template('admin/index.html')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('update_booking/<int:id>', methods=['POST'])
@permission_required(admin_permission)
def update_booking(id):
    depart_location = request.form.get('departLocation')
    destination_location = request.form.get('destinationLocation')
    depart_time = request.form.get('departTime')
    destination_time = request.form.get('destinationTime')
    fair_cost = request.form.get('fairCost')
    transport_type = request.form.get('transportType')
    images = request.files.getlist('images')
    main_image_id = request.form.get('main_image')

    listing = Listings.query.get(id)
    if listing:
        if depart_location:
            listing.depart_location = depart_location
        if destination_location:
            listing.destination_location = destination_location
        if depart_time:
            listing.depart_time = depart_time
        if destination_time:
            listing.destination_time = destination_time
        if fair_cost:
            listing.fair_cost = fair_cost
        if transport_type:
            listing.transport_type = transport_type

        try:
            ListingImages.set_main_image(listing.id, main_image_id)
            # Wrap upload of images in transaction in case any weird issues occur
            for image in images:
                new_image = ListingImages.save_image(image, listing.id)
                if new_image == False:
                    continue
                if new_image == None:
                    raise Exception("Failed to save image")
                
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            locations = Listings.get_all_locations()
            listing_information = Listings.search_listing(id)
            return render_template(
                'admin/edit_booking.html', 
                locations=locations, 
                listing=listing_information, 
                error="An error occurred while updating the booking."
            )
        
    locations = Listings.get_all_locations()
    flash('Successfully updated booking', 'success')
    return redirect(url_for('admin.manage_bookings'))



@bp.route('get_bookings', methods=['GET'])
@permission_required(admin_permission)
def get_bookings():
    query = db.session.query(Listings)

    depart_location = request.args.get('depart_location')
    destination_location = request.args.get('destination_location')
    depart_before_time = request.args.get('depart_before_time')
    arrive_after_time = request.args.get('arrive_after_time')
    min_fair_cost = request.args.get('min_fair_cost')
    max_fair_cost = request.args.get('max_fair_cost')
    transport_type = request.args.get('transport_type')

    if depart_location:
        depart_locations = depart_location.split(',')
        query = query.filter(Listings.depart_location.in_(depart_locations))
    if destination_location:
        destination_locations = destination_location.split(',')
        query = query.filter(Listings.destination_location.in_(destination_locations))
    if depart_before_time:
        query = query.filter(Listings.depart_time <= depart_before_time)
    if arrive_after_time:
        query = query.filter(Listings.destination_time >= arrive_after_time)
    if min_fair_cost:
        query = query.filter(Listings.fair_cost >= min_fair_cost)
    if max_fair_cost:
        query = query.filter(Listings.fair_cost <= max_fair_cost)
    if transport_type:
        query = query.filter(Listings.transport_type == transport_type)

    filtered_data = query.all()
    result = [
        {
            'id': listing.id,
            'depart_location': listing.depart_location,
            'depart_time': listing.depart_time.strftime("%H:%M"),
            'destination_location': listing.destination_location,
            'destination_time': listing.destination_time.strftime("%H:%M"),
            'fair_cost': listing.fair_cost,
            'transport_type': listing.transport_type
        } for listing in filtered_data
    ]
    
    return jsonify(result)

@bp.route('delete_booking', methods=['DELETE'])
@permission_required(admin_permission)
def delete_booking():
    http_code = 400
    booking_id = request.form.get('id')
    success = Listings.delete_listing(booking_id)

    if success:
        http_code = 200

    return jsonify(success), http_code
