from flask import request, jsonify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import os
# Avoid importing Role and RoleUsers here to prevent circular import

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)  # Add fs_uniquifier field

    # Import Role and RoleUsers only when defining the roles relationship
    from app.models.role_users import RoleUsers
    from app.models.role import Role
    roles = db.relationship('Role', secondary=RoleUsers.roles_users, backref=db.backref('users', lazy='dynamic'))

    @classmethod
    def create_user(cls, username, email, password, role_name='user'):
        from app.models import Role
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = cls(username=username, email=email, password=hashed_password, fs_uniquifier=os.urandom(32).hex())
    
        role = Role.query.filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()

        return new_user


    @classmethod
    def search_user_id(cls, user_id):
        return cls.query.get(user_id)
    
    @classmethod
    def search_user_by_email(cls, user_email):
        email_exist = cls.query.filter_by(email=user_email).first()
        
        return email_exist
    
    @classmethod
    def search_user_by_username(cls, user_name):
        user_exist = cls.query.filter_by(username=user_name).first()
        
        return user_exist
    
    @classmethod
    def change_user_password(cls, email, password):
        user = cls.search_user_by_email(email)

        if user is None:
            raise ValueError("Error")
