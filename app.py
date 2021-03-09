# TODO import things I'll need
from flask import Flask, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from form import consumerSignup_Form

from flask_login import LoginManager
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
from model import User
@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()

@app.route('/map')
def map():
    return render_template('Pages/map.html')


# Progam starts here

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
@app.route('/homepage')
def homepage():
    return render_template("Pages/homepage.html", title="Homepage - Edesia")

# About Us routing
@app.route('/about-us')
def about_us():
    return render_template("Pages/about-us.html", title="About Us - Edesia")

#Contact Us routing
@app.route('/contact-us')
def contact_us():
    return render_template("Pages/contact-us.html", title="Contact Us - Edesia")

# 2 - Functions

@app.route('/registration/<type_user>', methods=['GET', 'POST'])
def registration(type_user):
    if type_user == "consumer":
        registrationForm = consumerSignup_Form()
        print("sono arrivato qui 1")
        if registrationForm.validate_on_submit():
            print("sono arrivato qui2")
            new_user = User(name=registrationForm.name.data,
                            surname=registrationForm.surname.data,
                            email=registrationForm.email.data,
                            password_hash=registrationForm.password.data,
                            address=registrationForm.address.data,
                            phone_number=registrationForm.phone.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('homepage'))
        return render_template("Pages/signup-consumer.html", registrationForm=registrationForm)

    elif type_user == "supplier":
        return render_template("Pages/reg_supplier.html")

@app.route('/login')
def login():
    return render_template('Pages/login.html')


@app.route('/consumer')
def consumer():
    return render_template('Pages/profile_consumer.html')

@app.route('/farmer/orders')
def farmer_orders():
    return render_template('Pages/profile_supplier-orders.html')

@app.route('/farmer/products')
def farmer_products():
    return render_template('Pages/profile_supplier-products.html')

@app.route('/test')
def test():
    return render_template("Components/test.html")

@app.route('/results')
def research():
    return render_template("Pages/research_result.html")

@app.route('/farmer_store')
def farmer_store():
    return render_template("Pages/farmer_store.html")

if __name__ == '__main__':
    app.run(debug=True)
