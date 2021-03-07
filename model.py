from datetime import datetime
# Importing db created with sqlalchemy in app.py
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return "<User %r>" %self.id