from flask import render_template, redirect, url_for, Flask, jsonify
from app.api import bp
from app.models import User 
from sqlalchemy import text

@bp.route('/user_id/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        result = User.search_user_id(id)

        if result is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': result.user_id,
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
        result = User.create_user('ethan_root', 'ethan2.clay@live.uwe.ac.uk', 'password1234', 1)

        if result is None:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': result.user_id,
            'username': result.username,
            'email': result.email
        }
        return jsonify(user_data), 200
    
    #If something falls over throw nice error for debugging, will change for admin only users to see errors otherwise throw generic 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

