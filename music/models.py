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

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    category = db.Column(db.String(200))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='events')
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
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, primary_key=True)   
    # Define the one-to-many relationship with the Room model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    events_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def to_dict(self):
        h_dict = {
            b.name: str(getattr(self, b.name)) for b in self.__table__.columns
        }
        h_rooms = []
        # Add details of related Rooms to the Hotel's h_dict
        for room in self.rooms:
            room_data = {
                'id': room.id,
                'room_type': room.type,
                'num_rooms': room.num_rooms,
                'room_description': room.description,
                'room_rate': room.rate,
                'hotel_id': room.hotel_id
            }
            h_rooms.append(room_data)
        h_dict['rooms'] = h_rooms
        return h_dict

