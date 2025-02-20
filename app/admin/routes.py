from flask import render_template, redirect, url_for, request, jsonify, flash
from app import db
from app import admin_permission, permission_required, super_admin_permission
from app.models import Listings, ListingImages, User, Role
from app.admin import bp
from app.main.utils import generate_time_options

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
    locations = Listings.get_all_locations(True)
    return render_template('admin/manage_bookings.html', locations=locations)

@bp.route('/manage_bookings/edit/<int:id>')
@permission_required(admin_permission)
def edit_booking(id):
    locations = Listings.get_all_locations(True)
    listing_information = Listings.search_listing(id)

    time_options = generate_time_options()
    # Use the instance of the listing_information object to format the times
    depart_time_str = listing_information.depart_time.strftime("%H:%M")
    destination_time_str = listing_information.destination_time.strftime("%H:%M")
                                                             
    return render_template(
        'admin/edit_booking.html', 
        locations=locations, 
        listing=listing_information, 
        time_options=time_options, 
        depart_time_str=depart_time_str, 
        destination_time_str=destination_time_str
    )

@bp.route('/manage_users/edit/<int:id>')
@permission_required(super_admin_permission)
def edit_user(id):
    user = User.search_user_id(id)
    roles = Role.get_all_roles()                             
    return render_template(
        'admin/edit_user.html', 
        user=user,
        roles=roles
    )

@bp.route('/manage_users')
@permission_required(super_admin_permission)
def manage_users():
    return render_template('admin/manage_users.html')

@bp.route('/manage_user_bookings')
@permission_required(admin_permission)
def manage_user_bookings():
    return render_template('admin/index.html')


@bp.route('update_booking/<int:id>', methods=['POST'])
@permission_required(admin_permission)
def update_booking(id):
    depart_location = request.form.get('departLocation')
    destination_location = request.form.get('destinationLocation')
    depart_time = request.form.get('departTime')
    destination_time = request.form.get('destinationTime')
    economy_fair_cost = request.form.get('economyFairCost')
    business_fair_cost = request.form.get('businessFairCost')
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
        if economy_fair_cost:
            listing.economy_fair_cost = economy_fair_cost
        if business_fair_cost:
            listing.business_fair_cost = business_fair_cost
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
            locations = Listings.get_all_locations(True)
            listing_information = Listings.search_listing(id)
            return render_template(
                'admin/edit_booking.html', 
                locations=locations, 
                listing=listing_information, 
                error="An error occurred while updating the booking."
            )
        
    locations = Listings.get_all_locations(True)
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
            'economy_fair_cost': listing.economy_fair_cost,
            'business_fair_cost': listing.business_fair_cost,
            'transport_type': listing.transport_type
        } for listing in filtered_data
    ]
    
    return jsonify(result)


@bp.route('get_users', methods=['GET'])
@permission_required(super_admin_permission)
def get_users():
    all_users = User.get_all_users()

    result = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.name,
        } for user in all_users
    ]
    
    return jsonify(result)

@bp.route('create_listing', methods=['GET'])
@permission_required(admin_permission)
def create_listing():
    locations = Listings.get_all_locations(True)
    return render_template('admin/create_listing.html', locations=locations)


@bp.route('create_listing', methods=['POST'])
@permission_required(admin_permission)
def create_listing_post():
    # Extract form data
    depart_location = request.form.get('departLocation')
    destination_location = request.form.get('destinationLocation')
    depart_time = request.form.get('departTime')
    destination_time = request.form.get('destinationTime')
    fair_cost = request.form.get('fairCost')
    transport_type = request.form.get('transportType')
    images = request.files.getlist('images')

    # Create the listing instance
    new_listing = Listings(
        depart_location=depart_location,
        destination_location=destination_location,
        depart_time=depart_time,
        destination_time=destination_time,
        fair_cost=fair_cost,
        transport_type=transport_type
    )

    try:
        # Commit the new listing to get the ID
        db.session.add(new_listing)
        db.session.commit()

        # Save images and track the first one as the main image
        main_image_id = None

        for idx, image in enumerate(images):
            saved_image = ListingImages.save_image(image, new_listing.id)

            if not saved_image:
                continue

            if idx == 0:
                main_image_id = saved_image.id

        # Set main image if available
        if main_image_id:
            ListingImages.set_main_image(new_listing.id, main_image_id)

        db.session.commit()

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        locations = Listings.get_all_locations(True)
        flash('An error occurred while creating the booking. Please try again', 'error')
        return render_template('admin/create_listing.html', locations=locations)

    flash('Successfully created booking', 'success')
    return redirect(url_for('admin.manage_bookings'))


@bp.route('delete_booking', methods=['DELETE'])
@permission_required(admin_permission)
def delete_booking():
    http_code = 400
    booking_id = request.form.get('id')
    success = Listings.delete_listing(booking_id)

    if success:
        http_code = 200

    return jsonify(success), http_code

@bp.route('delete_user', methods=['DELETE'])
@permission_required(admin_permission)
def delete_user():
    http_code = 400
    user_id = request.form.get('id')
    success = User.delete_user(user_id)

    if success:
        http_code = 200

    return jsonify(success), http_code

@bp.route('/delete_image/<int:image_id>', methods=['POST'])
@permission_required(admin_permission)
def delete_image(image_id):
    try:
        image_to_delete = ListingImages.query.get_or_404(image_id)
        listing_id = image_to_delete.listing_id

        db.session.delete(image_to_delete)
        db.session.commit()

        new_main_image_id = None
        if image_to_delete.main_image:
            # Find another image for the same listing to set as main
            new_main_image = ListingImages.query.filter_by(listing_id=listing_id).first()
            if new_main_image:
                new_main_image.main_image = True
                db.session.commit()
                new_main_image_id = new_main_image.id

        return jsonify({'success': True, 'message': 'Image deleted successfully.', 'image_id': new_main_image_id})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@permission_required(super_admin_permission)
@bp.route('/update_user_field', methods=['POST'])
def update_user_field():
    data = request.get_json()
    user_id = data.get('user_id')
    field = data.get('field')
    value = data.get('value')
    user = User.query.get(user_id) 

    if user:
        if field == 'userName':
            user.username = value
        elif field == 'userEmail':
            user.email = value
        elif field == 'userRole':
            role = Role.query.get(value)
            if role:
                user.role_id = role.id
            else:
                return jsonify(success=False, message="Invalid role"), 400
        else:
            return jsonify(success=False, message="Invalid field"), 400

        try:
            db.session.commit()
            return jsonify(success=True)
        except Exception as e:
            db.session.rollback()
            return jsonify(success=False, message=str(e)), 500
    else:
        return jsonify(success=False, message="User not found"), 404