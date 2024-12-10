from flask import request, jsonify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.SmallInteger(), nullable=False)
    api_token = db.Column(db.String(255), nullable=True, unique=True)
    token_expiry = db.Column(db.DateTime(), nullable=True)

    @classmethod
    def create_user(cls, username, email, password, role_id = 1): # Role ID 1 is default for standard users
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') 
        new_user = cls(username=username, email=email, password=hashed_password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user

    @classmethod
    def search_user_id(cls, user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def search_user_by_email(cls, user_email):
        user_exist = cls.query.filter_by(email=user_email).first()
        
        return user_exist