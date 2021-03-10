# TODO import things I'll need
from flask import Flask, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Database configuration
app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

from model import *
from form import *

@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
# Adding the roles
    role_supplier = Role(name='Supplier')
    role_consumer = Role(name='Consumer')
    role_admin = Role(name='Admin')
    db.session.add_all([role_supplier, role_consumer, role_admin])
    db.session.commit()
# Adding a User
    newuser = User(name='Eugenio',
                email='pippo@gmail.com',
                password_hash=bcrypt.generate_password_hash('Pippooooo'),
                roleid=2
                )
    db.session.add(newuser)
    db.session.commit()
    newconsumer = Consumer(id=1,
                        consumer_name='Eugenio',
                        consumer_surname='Massini',
                        consumer_address='Paperopoli',
                        consumer_phone='3331234567')
    db.session.add(newconsumer)
    db.session.commit()


# Program starts here

# 1 - Basic Pages

# Error Page 404
@app.errorhandler(404)
def page_not_foud(e):
    return render_template('error/404.html')

# Error Page 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html')

# Homepagage routing
# TODO google maps search bar
@app.route('/')
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    researchForm = ResearchForm()
    if researchForm.validate_on_submit():
        return redirect(url_for('research', city=researchForm.city.data))
    return render_template("Pages/general/homepage.html", title="Homepage - Edesia", form=researchForm)

# About Us routing
@app.route('/about-us')
def about_us():
    return render_template("Pages/general/about-us.html", title="About Us - Edesia")

#Contact Us routing
@app.route('/contact-us')
def contact_us():
    return render_template("Pages/general/contact-us.html", title="Contact Us - Edesia")

# 2 - Functions Reg and Log

# Registration of the different Users
# based on the name of the user redirect to a different page and form

@app.route('/registration/<type_user>', methods=['GET', 'POST'])
def registration(type_user):

    if type_user == 'general':
        return render_template('Pages/registration/registration.html')

    if type_user == "consumer":
        registrationForm = ConsumerRegForm()
        if registrationForm.validate_on_submit():
            user = User(name=registrationForm.name.data,
                        email=registrationForm.email.data,
                        password_hash=bcrypt.generate_password_hash(registrationForm.password.data),
                        roleid=2)
            db.session.add(user)
            db.session.commit()
            id_user = User.query.filter_by(email=registrationForm.email.data).first()
            consumer = Consumer(id=id_user.id,
                                consumer_name=registrationForm.name.data,
                                consumer_surname=registrationForm.surname.data,
                                consumer_address=registrationForm.address.data,
                                consumer_phone=registrationForm.phone.data)

            db.session.add(consumer)
            db.session.commit()
            return redirect(url_for('homepage'))
        return render_template('Pages/registration/signup-consumer.html', registrationForm=registrationForm)

    if type_user == 'supplier':
        registrationForm = SupplierRegForm()
        if registrationForm.validate_on_submit():
            user = User(name=registrationForm.name.data,
                        email=registrationForm.email.data,
                        password_hash=bcrypt.generate_password_hash(registrationForm.password.data),
                        roleid=1)
            db.session.add(user)
            db.session.commit()
            id_user = User.query.filter_by(email=registrationForm.email.data).first()
            supplier = Supplier(id = id_user.id,
                                supplier_name=registrationForm.name.data,
                                piva=registrationForm.piva.data,
                                supplier_address=registrationForm.address.data,
                                supplier_phone=registrationForm.phone.data,
                                description= registrationForm.description.data)
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for('homepage'))
        return render_template('Pages/registration/signup-supplier.html', registrationForm=registrationForm)


# Login
# Based on the type of user redirect to the right page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            if user.roleid == 2:
                return redirect(url_for('consumer'))
            elif user.roleid == 1:
                return redirect(url_for('supplier'))
    return render_template('Pages/login.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# Consumer profile page
@app.route('/consumer')
@login_required
def consumer():
    return render_template('Pages/profile_consumer.html')

# Supplier page
@app.route('/supplier')
@login_required
def supplier():
    return render_template('Pages/profile_supplier-orders.html')

@app.route('/farmer/orders')
def farmer_orders():
    return render_template('Pages/profile_supplier-orders.html')

@app.route('/farmer/products')
def farmer_products():
    return render_template('Pages/profile_supplier-products.html')

# Research


@app.route('/test')
def test():
    return render_template("Components/test.html")

@app.route('/research/<city>')
def research(city):
    return render_template("Pages/research_result.html")

@app.route('/farmer_store')
def farmer_store():
    return render_template("Pages/farmer_store.html")


if __name__ == '__main__':
    app.run(debug=True)
