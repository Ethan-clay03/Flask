from flask import render_template, redirect, url_for, Flask, jsonify
from app.api import bp
from app.models import User, Listings
from sqlalchemy import text

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
        result = User.create_user('ethan_root', 'ethan2.clay@live.uwe.ac.uk', 'password1234', 1)

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
            "business_tickets": 10,
            "economy_tickets": 50
            }
        
        # Extract the required fields
        depart_location = data['depart_location']
        depart_time = datetime.strptime(data['depart_time'], '%Y-%m-%dT%H:%M:%S')  # Ensure date is in correct format
        destination_location = data['destination_location']
        destination_time = datetime.strptime(data['destination_time'], '%Y-%m-%dT%H:%M:%S')
        fair_cost = data['fair_cost']
        transport_type = data['transport_type']
        business_tickets = data['business_tickets']
        economy_tickets = data['economy_tickets']
        
        result = Listings.create_listing(depart_location, depart_time, destination_location, destination_time, fair_cost, transport_type, business_tickets, economy_tickets)

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