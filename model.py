from datetime import datetime
# Importing db created with sqlalchemy in app.py
from app import db
from flask_login import UserMixin
from app import login_manager

# 1 User management

# Role class is used to store the roles assigned to the users on Edesia
# Supplier 1, Consumer 2, Admin 3
class Role (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


# User class defines the general user, this table is intended to fasten the login
class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    roleid = db.Column(db.Integer, db.ForeignKey('role.id'))
    type = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<User %r>" % self.name

# Consumer specific class with its own attributes
class Consumer(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    consumer_name = db.Column(db.String(50), nullable=False)
    consumer_surname = db.Column(db.String(50), nullable=False)
    consumer_address = db.Column(db.String(50), nullable=False)
    consumer_phone = db.Column(db.String(12), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'consumer',
    }

# Supplier specific class with its own attributes
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

# Required by Flask-Login to handle the logged user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 2 Product manangement

class Product (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    box = db.Column(db.Boolean)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return "<Product %r>" % self.name


# 3 Order management

class Order (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumer.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    status = db.Column(db.String)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    pickup = db.Column(db.Boolean)

class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    quantity = db.Column(db.Float)
    partial_amount = db.Column(db.Float)


# 4 Contact Us message storage
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    request = db.Column(db.Text, nullable=False)