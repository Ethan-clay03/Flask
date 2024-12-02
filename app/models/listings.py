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
    listing_images = relationship("ListingImages", back_populates="listing_images")

    @classmethod
    def get_all_listings(cls):
        return cls.query.all()    
    
    @classmethod
    def create_listing(cls, depart_location, depart_time, destination_location, destination_time, fair_cost, transport_type, business_tickets, economy_tickets):
        new_flight = cls(depart_location=depart_location,
                         depart_time=depart_time,
                         destination_location=destination_location,
                         destination_time=destination_time,
                         fair_cost=fair_cost,
                         transport_type=transport_type,
                         business_tickets=business_tickets,
                         economy_tickets=economy_tickets)

        # Add the new flight to the database and commit
        db.session.add(new_flight)
        db.session.commit()
        return new_flight
        #return cls.query.all()   
    
    @classmethod    
    def get_top_listings(cls, amount_of_listings = 5):
         return cls.query.order_by(
            cls.economy_tickets,
            cls.business_tickets
        ).limit(amount_of_listings).all()
         
    