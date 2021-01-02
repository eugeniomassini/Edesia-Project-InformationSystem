from flask import Flask, render_template, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Database configuration
app.config['SECRET_KEY'] = 'kncjdiejdsfmsdasldfjwqop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # recommendation from pycharm

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
# app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

# Objects used
db = SQLAlchemy(app)  # database object
bcrypt = Bcrypt(app)  # to encrypt the use password
mail_object = Mail(app)  # mail object


# import classes from model
from model import User, Role, Consumer, Supplier, Review, ShoppingCart, Order, OrderLines, Message

# import forms
from form import ConsumerRegForm, SupplierRegForm, loginForm


# Create the Database setup (Before first request)
@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
    role_supplier = Role(name='Supplier')
    role_consumer = Role(name='Consumer')
    role_admin = Role(name='Admin')
    db.session.add_all([role_supplier, role_consumer, role_admin])
    db.session.commit()


# Send mail for confirmation of the registration
def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    print(msg)
    msg.html = render_template('welcome-mail.html', **kwargs)  # TODO modify welcome-mail.html
    mail_object.send(msg)


# Homepage
@app.route('/homepage')
@app.route('/home')
@app.route('/')
def homepage():
    return render_template("Pages/homepage.html", title="Homepage - Edesia")


# session login
def login():
    login_form = loginForm()
    if login_form.validate_on_submit():
        user_info = User.query.filter_by(email=login_form.email.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, login_form.password.data):
            session['user_id'] = user_info.id
            session['name'] = user_info.name
            session['email'] = user_info.email
            session['role_id'] = user_info.role_id

            if session['role_id'] == '2':
                return redirect(url_for('consumer'))

            elif session['role_id'] == '1':
                return redirect(url_for('supplier'))


# Consumer and Supplier registration
@app.route('/registration/<roleid>', methods=['POST', 'GET'])
def registration(roleid):
    if roleid == '2':
        name = None
        registerForm = ConsumerRegForm()
        if registerForm.validate_on_submit():
            name = registerForm.name.data
            session['name'] = registerForm.name.data
            session['email'] = registerForm.email.data
            password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
            new_user = User(name=registerForm.name.data,
                            email=registerForm.email.data,
                            password=password_2,
                            roleid=2)
            db.session.add(new_user)
            db.session.commit()
            user_info = User.query.filter_by(email=registerForm.email.data).first()
            session['user_id'] = user_info.id
            new_consumer = Consumer(id=user_info.id,
                                    consumer_name=registerForm.name.data,
                                    consumer_surname=registerForm.familyname.data,
                                    consumer_address=registerForm.address.data,
                                    consumer_phone=registerForm.phone.data)
            db.session.add(new_consumer)
            db.session.commit()

            # send welcome email
            send_mail(registerForm.email.data,
                      'You have registered successfully',
                      'mail',
                      name=registerForm.name.data,
                      email=registerForm.email.data,
                      password=registerForm.password.data)

            return redirect(url_for('login'))
        return render_template('Pages/signup-consumer.html', registerForm=registerForm, name=name)

    elif roleid == '1':
        name = None
        registerForm = SupplierRegForm()
        if registerForm.validate_on_submit():
            name = registerForm.name.data
            session['name'] = registerForm.name.data
            session['email'] = registerForm.email.data
            password_2 = bcrypt.generate_password_hash(registerForm.password.data).encode('utf-8')
            user_info = User(name=registerForm.name.data,
                             email=registerForm.email.data,
                             password=password_2,
                             roleid=1)
            db.session.add(user_info)
            db.session.commit()
            user_info = User.query.filter_by(email=registerForm.email.data).first()
            session['user_id'] = user_info.id
            new_supplier = Supplier(id=user_info.id,
                                    supplier_name=registerForm.name.data,
                                    supplier_address=registerForm.address.data,
                                    supplier_phone=registerForm.phone.data,
                                    piva=registerForm.piva.data,
                                    description=registerForm.description.data)
            db.session.add(new_supplier)
            db.session.commit()

            # send welcome email
            send_mail(registerForm.email.data,
                           'You have registered successfully',
                           'mail',
                           name=registerForm.name.data,
                           email=registerForm.email.data,
                           password=registerForm.password.data)

            return redirect(url_for('login'))
        return render_template('Pages/signup-supplier.html', registerForm=registerForm, name=name)





@app.route('/consumer')
def consumer():
    return render_template('Pages/profile_consumer.html')

@app.route('/supplier')
def supplier():
    return render_template('Pages/profile_supplier.html')

@app.route('/aboutUs')
def about_us():
    return render_template("Pages/aboutUs.html", title="About Us - Edesia")

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
    app.run()
