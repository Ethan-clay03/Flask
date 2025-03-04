from app import db
from flask_login import UserMixin
from app.logger import error_logger
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models import User

class Bookings(UserMixin, db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    seat_type = db.Column(db.String(50), nullable=False)
    num_seats = db.Column(db.Integer, nullable=False)
    cancelled = db.Column(db.Boolean, default=False)
    cancelled_date = db.Column(db.Date, nullable=False)
    refund_amount = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    depart_date = db.Column(db.Date, nullable=False)
    last_four_card_nums = db.Column(db.String(4), nullable=False)
    listing = relationship('Listings', back_populates='bookings')

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

    @classmethod
    def get_user_bookings(cls, user_id):
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            error_logger.error(f"Error retrieving bookings for user ID {user_id}: {e}")
            return None
        
    @classmethod
    def check_booking_user_ids_match(cls, booking_id, user_id):
        booking = cls.query.filter_by(id=booking_id, user_id=user_id).first()
        return booking is not None
    
    @classmethod
    def cancel_booking(cls, booking_id, refund_amount = 0):
        booking = cls.query.get(booking_id)
        if booking:
            booking.cancelled = True
            booking.cancelled_date = datetime.utcnow().date()
            booking.refund_amount = refund_amount
            db.session.commit()
            return True
        return False
    
    @classmethod
    def get_all_bookings(cls):
        return cls.query.all()
    
    @classmethod
    def get_all_bookings_with_user_table(cls):
        return cls.query.join(User, cls.user_id == User.id).add_columns(
            User.username
        ).all()

