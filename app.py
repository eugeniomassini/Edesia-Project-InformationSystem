# TODO import things I'll need
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # recommendation from pycharm

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

db = SQLAlchemy(app)  # database object
bcrypt = Bcrypt(app)  # to encrypt the use password
mail_object = Mail(app)  # mail object

from model import User, Role, Consumer, Supplier, Product, Review, Order, OrderLines, Message
from form import ConsumerRegForm, SupplierRegForm, loginForm, researchForm


@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
    role_supplier = Role(name='Supplier')
    role_consumer = Role(name='Consumer')
    role_admin = Role(name='Admin')
    db.session.add_all([role_supplier, role_consumer, role_admin])
    db.session.commit()

# Following lines only to pre-insert some users in the database without filling the form each time
    password1 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Fruit & Vegetables',
                     email='test1@gmail.com',
                     password=password1,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='test1@gmail.com').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Fruit & Vegetables',
                            supplier_address='Torino',
                            supplier_phone='0123456789',
                            piva='000000',
                            description='Local & Fresh Food')
    db.session.add(new_supplier)
    db.session.commit()
    password2 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Organic Food',
                     email='test2@gmail.com',
                     password=password2,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='test2@gmail.com').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Organic Food',
                            supplier_address='Milano',
                            supplier_phone='1234567890',
                            piva='222222',
                            description='Local & Fresh Vegetables')
    db.session.add(new_supplier)
    db.session.commit()
    password3 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    new_user = User(name='Elisa',
                    email='test3@gmail.com',
                    password=password3,
                    roleid=2)
    db.session.add(new_user)
    db.session.commit()
    user_info = User.query.filter_by(email='test3@gmail.com').first()
    session['user_id'] = user_info.id
    new_consumer = Consumer(id=user_info.id,
                            consumer_name='Elisa',
                            consumer_surname='Vassallo',
                            consumer_address='Torino',
                            consumer_phone='0123456789')
    db.session.add(new_consumer)
    db.session.commit()
    password3 = bcrypt.generate_password_hash('12345678').encode('utf-8')
    user_info = User(name='Organic Vegetables',
                     email='test4@gmail.com',
                     password=password3,
                     roleid=1)
    db.session.add(user_info)
    db.session.commit()
    user_info = User.query.filter_by(email='test4@gmail.com').first()
    session['user_id'] = user_info.id
    new_supplier = Supplier(id=user_info.id,
                            supplier_name='Organic Vegetables',
                            supplier_address='Torino',
                            supplier_phone='2345678901',
                            piva='333333',
                            description='Local Food')
    db.session.add(new_supplier)
    db.session.commit()
    new_product = Product(supplier_id='1',
                          price='1',
                          description='Tomato',
                          quantity='10')
    db.session.add(new_product)
    db.session.commit()
    new_product = Product(supplier_id='1',
                          price='2',
                          description='Orange',
                          quantity='15')
    db.session.add(new_product)
    db.session.commit()
    new_product = Product(supplier_id='2',
                          price='2',
                          description='Apple',
                          quantity='7')
    db.session.add(new_product)
    db.session.commit()
    new_product = Product(supplier_id='4',
                          price='1',
                          description='Potato',
                          quantity='20')
    db.session.add(new_product)
    db.session.commit()
# End of lines for pre-filling

# TODO homepage

@app.route('/homepage', methods=['POST', 'GET'])
def homepage():
    research_form = researchForm()
    if research_form.validate_on_submit():
        city = research_form.city.data
        session['city'] = research_form.city.data
        return redirect(url_for('research', city=city))
    return render_template("Pages/homepage.html", title="Homepage - Edesia", research_form=research_form)

@app.route('/registration/<type_user>')
def registration(type_user):
    if type_user == "consumer":
        return render_template("Pages/reg_consumer.html")
    elif type_user == "supplier":
        return render_template("Pages/reg_supplier.html")

@app.route('/consumer')
def consumer():
    return render_template('Pages/profile_consumer.html')

@app.route('/farmer')
def farmer():
    return render_template('Pages/profile_supplier.html')

@app.route('/aboutUs')
def about_us():
    return render_template("Pages/aboutUs.html", title="About Us - Edesia")

@app.route('/test')
def test():
    return render_template("Components/test.html")

@app.route('/results', methods=['GET'])
def research():
    city = request.args.get('city')
    localsuppliers = Supplier.query.filter_by(supplier_address=city).all()
    return render_template("Pages/research_result.html", localsuppliers=localsuppliers)

@app.route('/farmer_store/<farmerid>')
def farmer_store(farmerid):
    farmerproducts = Product.query.filter_by(supplier_id=farmerid).all()
    return render_template("Pages/farmer_store.html", farmerproducts=farmerproducts)

if __name__ == '__main__':
    app.run()
