from flask import request, jsonify
from app import db

class Listings(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    depart_location = db.Column(db.String(255), nullable=False)
    depart_time = db.Column(db.DateTime(), nullable=False)
    destination_location = db.Column(db.String(255), nullable=False)
    destination_time = db.Column(db.DateTime(), nullable=False)
    fair_cost = db.Column(db.Float(2), nullable=False)
    transport_type = db.Column(db.String(255), nullable=False)
    business_tickets = db.Column(db.Integer(), nullable=False)
    economy_tickets = db.Column(db.Integer(), nullable=False)

    @classmethod
    def get_all_listings(cls):
        return cls.query.all()    