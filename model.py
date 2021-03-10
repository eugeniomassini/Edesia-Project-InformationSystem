from datetime import datetime
# Importing db created with sqlalchemy in app.py
from app import db
from flask_login import UserMixin
from app import login_manager

class Role (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roleid = db.Column(db.Integer, db.ForeignKey('role.id'))
    type = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<User %r>" % self.name

class Consumer (db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    consumer_name = db.Column(db.String(50), nullable=False)
    consumer_surname = db.Column(db.String(50), nullable=False)
    consumer_address = db.Column(db.String(50), nullable=False)
    consumer_phone = db.Column(db.String(12), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'consumer',
    }

class Supplier (db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    supplier_name = db.Column(db.String(50), nullable=False)
    supplier_address = db.Column(db.String(50), nullable=False)
    supplier_phone = db.Column(db.String(12), nullable=False)
    piva = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'supplier',
    }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))