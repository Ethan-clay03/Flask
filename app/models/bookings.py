from app import db
from flask_login import UserMixin

class Bookings(UserMixin, db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    listing_id = db.Column(db.Integer, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    seat_type = db.Column(db.String(50), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False) 
    cancelled = db.Column(db.Boolean, default=False)
    booking_date = db.Column(db.Date, nullable=False)
    last_four_card_nums = db.Column(db.String(4), nullable=False)

    @staticmethod
    def create_booking(listing_id, user_id, amount_paid, seat_type, num_seats):
        try:
            new_booking = Bookings(
                user_id=user_id,
                listing_id=listing_id,
                amount_paid=amount_paid,
                seat_type=seat_type,
                num_seats=num_seats,
                cancelled=False
            )
            db.session.add(new_booking)
            db.session.commit()
            return new_booking
        except Exception as e:
            db.session.rollback()
            print(f"Error creating booking: {e}")
            return False

    @classmethod
    def search_booking(cls, id):
        return cls.query.get(id)
