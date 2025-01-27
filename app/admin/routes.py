from flask import render_template, redirect, url_for, request, jsonify
from app import db
from app import admin_permission, permission_required, super_admin_permission
from app.models import Listings
from app.admin import bp


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
    return render_template('admin/manage_bookings.html')

@bp.route('/manage_users')
@permission_required(super_admin_permission)
def manage_users():
    return render_template('admin/index.html')

@bp.route('/manage_user_bookings')
@permission_required(admin_permission)
def manage_user_bookings():
    return render_template('admin/index.html')

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