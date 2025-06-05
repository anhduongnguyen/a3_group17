from . import db
from datetime import datetime, timezone
from flask_login import UserMixin
import random, string

# Tables outline

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    contact_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    events = db.relationship('Event', backref='owner', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Open")  

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy='dynamic', order_by='desc(Comment.timestamp)')
    ## calculate the amount of tickets remaining
    def tickets_remaining(self):
        booked = sum(booking.quantity for booking in self.bookings)
        return max(0, self.capacity - booked)
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    
    def generate_booking_code(self, length=6):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Booking.query.filter_by(booking_code=code).first():
                return code


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


