from flask import request, jsonify
from app.api import bp
from app import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

    @classmethod
    def create_user(cls, username, email):
        new_user = cls(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def search_user_id(cls, user_id):
        return cls.query.get(user_id)