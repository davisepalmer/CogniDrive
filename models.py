from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #date = db.Column(db.DateTime(timezone=True),default=func.now()) maybe fix later
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#THESE CASES ARE PURPOSEFUL, even in strings
