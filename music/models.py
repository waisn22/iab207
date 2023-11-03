
from flask_login import UserMixin
from datetime import datetime
from . import db
class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Ticket', backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    venue = db.Column(db.String(200))
    date = db.Column(db.Date)
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time) 
    image = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2))
    category = db.Column(db.String(80))
    status = db.Column(db.String(80))
    ticketquantity = db.Column(db.Integer)
    boughttickets = db.Column(db.Integer)

    comments = db.relationship('Comment', backref='events')
    bookings = db.relationship('Ticket', backref='events')

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	# string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(400), index=True, unique=True, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2))
    event_name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Ticket: {self.text}"

