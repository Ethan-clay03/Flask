from sqlalchemy.orm import relationship
from sqlalchemy import Time
from app import db
from sqlalchemy.sql import text

class Listings(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    depart_location = db.Column(db.String(255), nullable=False)
    depart_time = db.Column(Time, nullable=False)
    destination_location = db.Column(db.String(255), nullable=False)
    destination_time = db.Column(Time, nullable=False)
    economy_fair_cost = db.Column(db.Float(), nullable=False) 
    business_fair_cost = db.Column(db.Float(), nullable=False) 
    transport_type = db.Column(db.String(255), nullable=False)
    listing_images = relationship("ListingImages", back_populates="listing", cascade="all, delete-orphan")

    @classmethod
    def get_all_listings(cls):
        return cls.query.all()

    @classmethod
    def get_all_locations(cls, ordered=False):
        all_locations = text("SELECT depart_location AS location FROM listings UNION SELECT destination_location AS location FROM listings")
        result = db.session.execute(all_locations)
        listed_results = [location[0] for location in result]

        if ordered:
            return sorted(listed_results)
        
        return listed_results

    @classmethod
    def create_listing(cls, depart_location, depart_time, destination_location, destination_time, fair_cost, transport_type):
        new_flight = cls(depart_location=depart_location,
                         depart_time=depart_time,
                         destination_location=destination_location,
                         destination_time=destination_time,
                         fair_cost=fair_cost,
                         transport_type=transport_type)

        db.session.add(new_flight)
        db.session.commit()
        return new_flight

    @classmethod
    def get_top_listings(cls, amount_of_listings=5):
        return cls.query.limit(amount_of_listings).all()
    
    @classmethod
    def delete_listing(cls, booking_id = None):

        listing =  cls.search_listing(booking_id)

        if listing:
            db.session.delete(listing)
            db.session.commit()
            return True
        
        return False
    
    @classmethod
    def search_listing(cls, listing_id = None):
        if listing_id == None:
            return False
    
        return cls.query.get(listing_id)

    @classmethod
    def to_dict(self):
        return {
            'id': self.id,
            'depart_location': self.depart_location,
            'depart_time': self.depart_time,
            'destination_location': self.destination_location,
            'destination_time': self.destination_time,
            'transport_type': self.transport_type,
            'economy_fair_cost': self.economy_fair_cost,
            'business_fair_cost': self.business_fair_cost
        }
        
