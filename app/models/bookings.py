from app import db
from flask_login import UserMixin
from app.logger import error_logger
from datetime import datetime

class Bookings(UserMixin, db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    listing_id = db.Column(db.Integer, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    seat_type = db.Column(db.String(50), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False) 
    cancelled = db.Column(db.Boolean, default=False)
    cancelled_date = db.Column(db.Date, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    depart_date = db.Column(db.Date, nullable=False)
    last_four_card_nums = db.Column(db.String(4), nullable=False)

    @classmethod
    def create_booking(cls, listing_id, user_id, amount_paid, seat_type, num_seats, depart_date, last_four_card_nums):
        today_date = datetime.now().strftime('%Y-%m-%d')
        try:
            new_booking = cls(
                user_id=user_id,
                listing_id=listing_id,
                amount_paid=amount_paid,
                seat_type=seat_type,
                num_seats=num_seats,
                cancelled=False,
                booking_date=today_date,
                depart_date=depart_date,
                last_four_card_nums=last_four_card_nums
            )
            db.session.add(new_booking)
            db.session.commit()
            return new_booking
        except Exception as e:
            db.session.rollback()
            error_logger.error(f"Error creating booking: {e}")
            return False

    @classmethod
    def search_booking(cls, id):
        return cls.query.get(id)
