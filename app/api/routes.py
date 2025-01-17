from flask import jsonify, request
from app.api import bp
from app.models import User, Listings
from app import db
from app import admin_permission, permission_required, super_admin_permission
import json

@bp.route('/user_id/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        result = User.search_user_id(id)

        if result is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': result.id,
            'username': result.username,
            'email': result.email
        }
        return jsonify(user_data), 200
    
    #If something falls over throw nice error for debugging, will change for admin only users to see errors otherwise throw generic 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/user/create', methods=['GET'])
def create_user():
    try:
        #Hardcoded for now as when running upgrade on new db no users exist yet, will change at some point
        result = User.create_user('ethan_root', 'ethan2.clay@live.uwe.ac.uk', 'password1234', 2) # Role ID 2 is for admins

        if result is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': result.id,
            'username': result.username,
            'email': result.email
        }
        return jsonify(user_data), 200
    
    #If something falls over throw nice error for debugging, will change for admin only users to see errors otherwise throw generic 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/listing/create', methods=['GET'])
def create_listing():
    
    #Temporary import
    from datetime import datetime
    
    
    try:
        #Hardcoded for now as when running upgrade on new db no users exist yet, will change at some point
        data = {
            "depart_location": "New York",
            "depart_time": "2024-12-01T08:00:00",
            "destination_location": "London",
            "destination_time": "2024-12-01T18:00:00",
            "fair_cost": 500.00,
            "transport_type": "Airplane",
            }
        
        # Extract the required fields
        depart_location = data['depart_location']
        depart_time = datetime.strptime(data['depart_time'], '%Y-%m-%dT%H:%M:%S')  # Ensure date is in correct format
        destination_location = data['destination_location']
        destination_time = datetime.strptime(data['destination_time'], '%Y-%m-%dT%H:%M:%S')
        fair_cost = data['fair_cost']
        transport_type = data['transport_type']
        
        result = Listings.create_listing(depart_location, depart_time, destination_location, destination_time, fair_cost, transport_type)

        if result is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'depart_location': result.depart_location,
            'depart_time': result.depart_time,
            'id': result.id
        }
        return jsonify(user_data), 200
    
    #If something falls over throw nice error for debugging, will change for admin only users to see errors otherwise throw generic 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Sample data
data = [
    {"depart_location": "Tiger Nixon", "depart_time": "System Architect", "destination_location": "Edinburgh", "destination_time": 61, "fair_cost": "2011-04-25", "transport_type": "$320,800"},
]

@bp.route('get_data', methods=['GET'])
@permission_required(super_admin_permission)
def get_data():
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
            'depart_location': listing.depart_location,
            'depart_time': listing.depart_time.strftime("%H:%M"),
            'destination_location': listing.destination_location,
            'destination_time': listing.destination_time.strftime("%H:%M"),
            'fair_cost': listing.fair_cost,
            'transport_type': listing.transport_type
        } for listing in filtered_data
    ]

    return jsonify(result)
