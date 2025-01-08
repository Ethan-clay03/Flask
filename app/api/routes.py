from flask import jsonify, request
from app.api import bp
from app.models import User, Listings
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

# Sample data
data = [
    {"Name": "Tiger Nixon", "Position": "System Architect", "Office": "Edinburgh", "Age": 61, "StartDate": "2011-04-25", "Salary": "$320,800"},
    {"Name": "Garrett Winters", "Position": "Accountant", "Office": "Tokyo", "Age": 63, "StartDate": "2011-07-25", "Salary": "$170,750"},
    {"Name": "Ashton Cox", "Position": "Junior Technical Author", "Office": "San Francisco", "Age": 66, "StartDate": "2009-01-12", "Salary": "$86,000"},
    {"Name": "Cedric Kelly", "Position": "Senior Javascript Developer", "Office": "Edinburgh", "Age": 22, "StartDate": "2012-03-29", "Salary": "$433,060"},
    {"Name": "Airi Satou", "Position": "Accountant", "Office": "Tokyo", "Age": 33, "StartDate": "2008-11-28", "Salary": "$162,700"},
    {"Name": "Brielle Williamson", "Position": "Integration Specialist", "Office": "New York", "Age": 61, "StartDate": "2012-12-02", "Salary": "$372,000"},
    {"Name": "Herrod Chandler", "Position": "Sales Assistant", "Office": "San Francisco", "Age": 59, "StartDate": "2012-08-06", "Salary": "$137,500"},
    {"Name": "Rhona Davidson", "Position": "Integration Specialist", "Office": "Tokyo", "Age": 55, "StartDate": "2010-10-14", "Salary": "$327,900"},
    {"Name": "Colleen Hurst", "Position": "Javascript Developer", "Office": "San Francisco", "Age": 39, "StartDate": "2009-09-15", "Salary": "$205,500"},
    {"Name": "Sonya Frost", "Position": "Software Engineer", "Office": "Edinburgh", "Age": 23, "StartDate": "2008-12-13", "Salary": "$103,600"},
    {"Name": "Jena Gaines", "Position": "Office Manager", "Office": "London", "Age": 30, "StartDate": "2008-12-19", "Salary": "$90,560"},
    {"Name": "Quinn Flynn", "Position": "Support Lead", "Office": "Edinburgh", "Age": 22, "StartDate": "2013-03-03", "Salary": "$342,000"},
    {"Name": "Charde Marshall", "Position": "Regional Director", "Office": "San Francisco", "Age": 36, "StartDate": "2008-10-16", "Salary": "$470,600"},
    {"Name": "Haley Kennedy", "Position": "Senior Marketing Designer", "Office": "London", "Age": 43, "StartDate": "2012-12-18", "Salary": "$313,500"},
    {"Name": "Tatyana Fitzpatrick", "Position": "Regional Director", "Office": "London", "Age": 19, "StartDate": "2010-03-17", "Salary": "$385,750"},
    {"Name": "Michael Silva", "Position": "Marketing Designer", "Office": "London", "Age": 66, "StartDate": "2012-11-27", "Salary": "$198,500"},
    {"Name": "Paul Byrd", "Position": "Chief Financial Officer (CFO)", "Office": "New York", "Age": 64, "StartDate": "2010-06-09", "Salary": "$725,000"},
    {"Name": "Gloria Little", "Position": "Systems Administrator", "Office": "New York", "Age": 59, "StartDate": "2009-04-10", "Salary": "$237,500"},
    {"Name": "Bradley Greer", "Position": "Software Engineer", "Office": "London", "Age": 41, "StartDate": "2012-10-13", "Salary": "$132,000"},
    {"Name": "Dai Rios", "Position": "Personnel Lead", "Office": "Edinburgh", "Age": 35, "StartDate": "2012-09-26", "Salary": "$217,500"},
    {"Name": "Jenette Caldwell", "Position": "Development Lead", "Office": "New York", "Age": 30, "StartDate": "2011-09-03", "Salary": "$345,000"},
]

@bp.route('/api/get_data', methods=['GET'])
def get_data():
    min_age = request.args.get('min_age', type=int, default=0)
    max_age = request.args.get('max_age', type=int, default=100)
    
    filtered_data = [entry for entry in data if min_age <= entry['Age'] <= max_age]
    return jsonify(filtered_data)

