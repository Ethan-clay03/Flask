from app import db

class ListingAvailability(db.Model):
    __tablename__ = 'listing_availability'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    air_economy_seats = db.Column(db.Integer, nullable=False)
    air_business_seats = db.Column(db.Integer, nullable=False)

    @staticmethod
    def check_availability(listing_id, date, seat_type, num_seats):
        availability = ListingAvailability.query.filter_by(
            listing_id=listing_id,
            date=date
        ).first()

        if availability == None:
            ListingAvailability.create_availability(listing_id, date)

            # Fetch the newly created availability row
            availability = ListingAvailability.query.filter_by(
                listing_id=listing_id,
                date=date
            ).first()

        if seat_type == 'business':
            if availability.air_business_seats >= num_seats:
                return True
            else:
                return availability.air_business_seats
        else:
            if availability.air_economy_seats >= num_seats:
                return True
            else:
                return availability.air_economy_seats

    @staticmethod
    def update_availability(listing_id, date, seat_type, num_seats):
        availability = ListingAvailability.query.filter_by(
            listing_id=listing_id,
            date=date
        ).first()
        if availability:
            if seat_type == 'business':
                availability.air_business_seats -= num_seats
            else:
                availability.air_economy_seats -= num_seats
            db.session.commit()

    @staticmethod
    def create_availability(listing_id, date, economy_seats = 104, business_seats = 26):
        try:
            new_availability = ListingAvailability(
                listing_id=listing_id,
                date=date,
                air_economy_seats=economy_seats, # Defaults as set per the spec, calling create_availibility you can override the values 
                air_business_seats=business_seats 
            )
            db.session.add(new_availability)
            db.session.commit()
            return new_availability
        except Exception as e:
            db.session.rollback()
            print(f"Error creating availability: {e}")
            return None
