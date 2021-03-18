from datetime import timedelta
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message
from flask_moment import Moment

app = Flask(__name__)

#Setting the Google Maps API from the venv variable
#API required for the research
app.config['GMAPS_API'] = os.environ.get('GMAPS_API')

# Secret Key for Flask-WTF
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

#Login tools
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# login_manager.init_app(app)

from model import *
from form import *


# Function to send an Email
# Can be implemented to send send different tipe of emails
def send_mail(to, subject, **kwargs):
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template('welcome-mail.html', **kwargs)
    mail.send(msg)

# Before starting the program this function is elaborated
# Creating the database variables
# For demonstration purpose we created different users, orders, products and reviews
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

# Adding Users

    users = [
        {'name': "Eugenio", 'surname':"Massini"},
        {'name': "Aleix", 'surname': "Carbonel"},
        {'name': "Chiara", 'surname': "Nicolini"},
        {'name': "Anna", 'surname': "Neirotti"},
        {'name': "Valeria", 'surname': "Porzio"},
        {'name': "Elisa", 'surname': "Vassallo"}
    ]

    for user in users:
            mail = user['name'].lower()+user['surname'].lower()+'@mail.com'
            user_db = User(name=user['name'],
                        email=mail,
                        password_hash=bcrypt.generate_password_hash('12345678'),
                        roleid=2)
            db.session.add(user_db)
            db.session.commit()
            user_id = User.query.order_by(User.id.desc()).first()
            consumer = Consumer(id=user_id.id,
                           consumer_name=user['name'],
                           consumer_surname=user['surname'],
                           consumer_address='Corso Duca degli Abruzzi, 24, Turin',
                           consumer_phone='3331234567')
            db.session.add(consumer)
            db.session.commit()

#Add Suppliers

    suppliers = [
        {'name': "Eugenio", 'surname': "Massini"},
        {'name': "Aleix", 'surname': "Carbonel"},
        {'name': "Chiara", 'surname': "Nicolini"},
        {'name': "Anna", 'surname': "Neirotti"},
        {'name': "Valeria", 'surname': "Porzio"},
        {'name': "Elisa", 'surname': "Vassallo"}
    ]

    for user in suppliers:
        description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        name = user['name'] +' '+user['surname']+"'s farm"
        mail = user['name'].lower() + user['surname'].lower() + 'farm@mail.com'
        user_db = User(name=name,
                       email=mail,
                       password_hash=bcrypt.generate_password_hash('12345678'),
                       roleid=1)
        db.session.add(user_db)
        db.session.commit()
        user_id = User.query.order_by(User.id.desc()).first()
        supplier = Supplier(id= user_id.id,
                            supplier_name=name,
                            supplier_address='Turin, Metropolitan City of Turin, Italy',
                            supplier_city='Turin, Metropolitan City of Turin, Italy',
                            supplier_phone='0123456789',
                            piva='000000',
                            description=description)
        db.session.add(supplier)
        db.session.commit()


#Add products

    products = [
        {'name': "Tomatoes", 'price': 5.00, 'quantity': 20.00},
        {'name': "Potatoes", 'price': 3.00, 'quantity': 25.00},
        {'name': "Beets", 'price': 4.00, 'quantity': 15.00},
    ]

    for product in products:
        users = User.query.filter_by(roleid=1).all()
        for user in users:
            product_db = Product(supplier_id=user.id,
                    name=product['name'],
                    price=product['price'],
                    quantity=product['quantity'],
                    description=None,
                    box=False)
            db.session.add(product_db)
            db.session.commit()


    for i in range(2):
        description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        users = User.query.filter_by(roleid=1).all()
        for user in users:
            product_db = Product(supplier_id=user.id,
                                 name='Special Box',
                                 price=20.00,
                                 quantity=4.00,
                                 description=description,
                                 box=True)
            db.session.add(product_db)
            db.session.commit()

# Add Orders
    consumers = Consumer.query.all()
    suppliers = Supplier.query.all()

    for consumer in consumers:
        for supplier in suppliers:
            order = Order(consumer_id=consumer.id,
                           supplier_id=supplier.id,
                           amount=15.00,
                           date=datetime.utcnow(),
                           delivery_date=datetime.now() + timedelta(days=1)
                           )
            db.session.add(order)
            db.session.commit()
            order_id = Order.query.order_by(Order.id.desc()).first()
            orderline = OrderLine(order_id=order_id.id,
                                   supplier_id=supplier.id,
                                   product_id=2,
                                   product_name='Beats',
                                   quantity=3.00,
                                   partial_amount=9.00)
            db.session.add(orderline)
            db.session.commit()

    orders = Order.query.all()
    for order in orders:
        review = Review(order_id=order.id,
                        consumer_id=order.consumer_id,
                        supplier_id=order.supplier_id,
                        text='Everything was good')
        order.review = True
        db.session.add(review)
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

# Homepage routing and beginning of the research process
@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    session['GMAPS_API'] = app.config['GMAPS_API']
    researchForm = ResearchForm()
    if researchForm.validate_on_submit():
        return redirect(url_for('research', city=researchForm.city.data))
    return render_template("Pages/general/homepage.html", title="Homepage - Edesia", form=researchForm)

# About Us routing, static page
@app.route('/about-us')
def about_us():
    return render_template("Pages/general/about-us.html", title="About Us - Edesia")

# Contact Us routing
@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    form=ContactUsForm()
    if form.validate_on_submit():
        message = AssistanceMessage(name=form.name.data,
                                    surname=form.surname.data,
                                    email=form.email.data,
                                    request=form.message.data)
        db.session.add(message)
        db.session.commit()
        flash('Success')
        return redirect(url_for('contact_us'))

    return render_template("Pages/general/contact-us.html", title="Contact Us - Edesia", form=form)

# 2 - Functions Reg and Log

# Registration of the different Users
# Based on the name of the user redirect to a different page and form
@app.route('/registration/<type_user>', methods=['GET', 'POST'])
def registration(type_user):

    # general page where you can decide the user role
    if type_user == 'general':
        return render_template('Pages/registration/registration.html', title= "Registration Page")

    # redirecting to the consumer form specific for user
    # first registering the User and than the Consumer
    # we need to create the User before to get the user id wich is a foreign key for Consumer in the model
    if type_user == "consumer":
        registrationForm = ConsumerRegForm()
        if registrationForm.validate_on_submit():
            user = User(name=registrationForm.name.data,
                        email=registrationForm.email.data,
                        password_hash=bcrypt.generate_password_hash(registrationForm.password.data), # hashing the password with bcrypt for safety
                        roleid=2) # the roleid is based on the order of the setupdb()
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
            # send email
            send_mail(registrationForm.email.data,
                      'You have registered successfully',
                      name=registrationForm.name.data,
                      username=registrationForm.email.data,
                      password=registrationForm.password.data)
            return redirect(url_for('login'))
        return render_template('Pages/registration/signup-consumer.html', registrationForm=registrationForm, title="Registration-Consumer")

    # redirecting to the supplier form specific for user
    # first registering the User and than the Supplier
    # we need to create the User before to get the user id wich is a foreign key for Supplier in the model
    if type_user == 'supplier':
        registrationForm = SupplierRegForm()
        if registrationForm.validate_on_submit():
            user = User(name=registrationForm.name.data,
                        email=registrationForm.email.data,
                        password_hash=bcrypt.generate_password_hash(registrationForm.password.data), # hashing the password with bcrypt for safety
                        roleid=1) # the roleid is based on the order of the setupdb()
            db.session.add(user)
            db.session.commit()
            id_user = User.query.filter_by(email=registrationForm.email.data).first()
            # this code saves the city from the address
            city = str(registrationForm.address.data)
            address = city.split(',')
            # we need to divide two cases to be sure to get the right city
            if any(str.isdigit(c) for c in address[1]): # if the number in the address we need to remove it
                to_remove = address[0] + ',' + address[1] + ', '
            else: # if not we just need to remove the road from address
                to_remove = address[0] + ', '

            city = city.replace(to_remove, '') # new city without the street and the civic number
            print city
            supplier = Supplier(id = id_user.id,
                                supplier_name=registrationForm.name.data,
                                piva=registrationForm.piva.data,
                                supplier_address=registrationForm.address.data,
                                supplier_city=city,
                                supplier_phone=registrationForm.phone.data,
                                description= registrationForm.description.data)
            db.session.add(supplier)
            db.session.commit()
            # send email
            send_mail(registrationForm.email.data,
                      'You have registered successfully',
                      name=registrationForm.name.data,
                      username=registrationForm.email.data,
                      password=registrationForm.password.data)
            return redirect(url_for('login'))
        return render_template('Pages/registration/signup-supplier.html', registrationForm=registrationForm, title="Registration-Supplier")


# Login
# Based on the type of user redirect to the right page
# Managed with Flask-Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password_hash, form.password.data): # hashing the password with bcrypt for safety
            login_user(user) # flask-login logs the user
            session['roleid']=user.roleid
            session['id']=user.id
            if user.roleid == 2:
                return redirect(url_for('consumer', id=user.id))
            elif user.roleid == 1:
                return redirect(url_for('supplier', id=user.id, page='orders'))
    return render_template('Pages/login.html', form=form, title="Login")

# Logout
@app.route('/logout')
@login_required # decorator from flask-login
def logout():
    logout_user() # flask-login logs out the user
    return redirect(url_for('homepage'))

# Consumer profile page
@app.route('/consumer/<int:id>')
@login_required # decorator from flask-login
def consumer(id):
    consumer = Consumer.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    orders = Order.query.filter_by(consumer_id=id).order_by(Order.id.desc()).all()
    l_order_cons =[] #list to contain the following object

    class OrderCons(): # object to simplify the storage of the order data
        def __init__(self, order, content, supplier):
            self.order = order
            self.content = content
            self.supplier = supplier

    for o in orders: # for each order
        products = [] # we create a list of product
        lines = OrderLine.query.filter_by(order_id=o.id).all() # lines contains all the products in that order
        supplier = Supplier.query.filter_by(id=o.supplier_id).first()

        for l in lines:
            products.append(l) # filling the list of products with all the product for that specific order

        l_order_cons.append(OrderCons(o, products, supplier)) # storing the information i need for each order

    return render_template('Pages/profile/profile_consumer-orders.html', consumer=consumer, user=user, orders=l_order_cons, title="Consumer-Profile")

# Review page
# Allowing the user to create a review with a simple like the previous
@app.route('/consumer/<int:id>/review/order_id=<int:order_id>', methods=['GET', 'POST'])
@login_required # decorator from flask-login
def consumer_review(id, order_id):
    consumer = Consumer.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    order = Order.query.filter_by(id=order_id).first()

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(order_id=order.id, # assosciated with a specific order
                        consumer_id=id, # from a specific consumer
                        supplier_id=order.supplier_id,# from a specific farmer
                        text= form.text.data) # content of the review
        order.review=True
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('consumer', id=id))

    return render_template('Pages/profile/profile_consumer-review.html', consumer=consumer, user=user, form=form, order=order, title="Review")

# Supplier page
# based on the page passed in the url we render the page
@app.route('/supplier/<int:id>/<page>', methods=['GET', 'POST'])
@login_required # decorator from flask-login
def supplier(id, page):
    supplier = Supplier.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    # default page to manage all the orders
    if page == "orders": # order displayed as for the consumer
        orders = Order.query.filter_by(supplier_id=id).all()
        l_order_cons = []


        class OrderCons():
            def __init__(self, order, content, consumer):
                self.order = order
                self.content = content
                self.consumer = consumer

        for o in orders:
            products = []
            lines = OrderLine.query.filter_by(order_id=o.id).all()
            consumer = Consumer.query.filter_by(id=o.consumer_id).first()

            for l in lines:
                products.append(l)

            l_order_cons.append(OrderCons(o, products, consumer))
        return render_template('Pages/profile/profile_supplier-orders.html', supplier=supplier, user=user, orders=l_order_cons, title="Supplier-Profile")
    elif page == "products": # page with all the prodcuts, for the rendering part look at the template
        products = Product.query.filter_by(supplier_id=id).all()
        return render_template('Pages/profile/profile_supplier-products.html', supplier=supplier, user=user, products=products, title="Supplier-Profile")
    elif page == "add-product": # allowing to add a product
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(supplier_id=id,
                              price=form.price.data,
                              name=form.name.data,
                              quantity=form.quantity.data,
                              box=False) # based on the page we know if the supplier is creating a box or not
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('supplier', id=id, page='products'))
        return render_template('Pages/profile/profile-supplier_addProduct.html', supplier=supplier, user=user, form=form, title="Supplier-Profile")
    elif page == "add-box": # allowing to add a box
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(supplier_id=id,
                              price=form.price.data,
                              description=form.description.data,
                              name=form.name.data,
                              quantity=form.quantity.data,
                              box=True) # based on the page we know if the supplier is creating a box or not
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('supplier', id=user.id, page='products'))
        return render_template('Pages/profile/profile-supplier_addBox.html', supplier=supplier, user=user, form=form, title="Supplier-Profile")

# Edit page for product
# getting all the info and displaying the form pre compiled
# with the previous info to be modified
@app.route('/supplier/<int:id>/edit-product=<int:product_id>', methods=['GET', 'POST'])
@login_required # decorator from flask-login
def supplier_edit_product(id, product_id):
    supplier = Supplier.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    product = Product.query.filter_by(id=product_id).first()
    products = Product.query.filter_by(supplier_id=id).all()
    form = EditProduct()

    if form.validate_on_submit():
        product.name = form.name.data
        product.quantity = form.quantity.data
        product.price = form.price.data
        product.description = form.description.data

        db.session.commit()
        return redirect(url_for('supplier', id=id, page='products'))

    # registering the previous info to be modified
    form.name.data = product.name
    form.quantity.data = product.quantity
    form.price.data = product.price
    form.description.data = product.description
    # rendering the tamplate with the form instead of the text
    return render_template('Pages/profile/profile_supplier-edit_products.html', supplier=supplier, user=user, form=form, products=products, product_id=product_id, title="Supplier-Profile")


# 3 Ordering process
# Research, Farmer store, place order

# 1 Step: Research
@app.route('/research/<city>')
def research(city):
    suppliers = Supplier.query.filter_by(supplier_city=city).all() # for now just based on the cities
    return render_template("Pages/research_result.html", suppliers=suppliers, title="Results")

# 2 Step: Display Farmer Store
# Pass the id the farmer to show his page
# Dinamically entering min_entries to create the form for the order
@app.route('/farmer_store/<int:id>', methods=['GET', 'POST'])
def farmer_store(id):
    supplier = Supplier.query.filter_by(id=id).first()
    products = Product.query.filter(Product.supplier_id==id, Product.box==False, Product.quantity>0.0).all()
    boxes = Product.query.filter(Product.supplier_id==id, Product.box==True, Product.quantity>0.0).all()

    #setting this dinamically based on the inventory
    min_entries = len(products)+len(boxes)

    #Creating a LocalForm based on the Order form to store the min_entries
    class LocalForm(OrderForm):pass
    LocalForm.order = FieldList(FormField(OrderEntryForm), min_entries=min_entries) # min_entries represent the minimum istances of the FormField that will be shown

    form=LocalForm()

    reviews = Review.query.filter_by(supplier_id=id).all() # query the reviews to be shown in the page

    return render_template("Pages/farmer_store.html", supplier=supplier, products=products, boxes=boxes, form=form, reviews=reviews, title="Supplier-Store")

# 3 Step: Elaborate and Validate the order
# Processing everything about the order here
# requesting the form and controlling availability
@app.route('/order/confirmation/<int:id>', methods=['POST'])
@login_required # decorator from flask-login, page accesible only if logged in
def order_func(id):
    # order available only by consumer
    if session['roleid'] == 1: # if supplier redirected
        return redirect(url_for('homepage'))

    supplier = Supplier.query.filter_by(id=id).first()
    products = Product.query.filter_by(supplier_id=id, box=False).all()
    boxes = Product.query.filter_by(supplier_id=id, box=True).all()
    n = len(products)+len(boxes)
    # requesting the form
    order = request.form
    # iterating on it to create a dictionary
    order_dict = { x:order[x] for x in order if "order-" in x}
    amount = 0.0 # setting the total amount for the order
    bought_l = [] # list that will contain the bought prodcut
    class Bought(): # object created to simplify the data storage
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity


    # accessing with index to match the right product with the right FormField
    for i in range(n):
        str = 'order-%d' % i # creating a string to check the key based on the index
        for key in order_dict.iterkeys():
            # for the product we have to check if a box, if it's to order and store the quantity
            if str in key:
                quantity = str + '-quantity'
                to_order = str + '-to_order'
                if 'box' in key: # here we know that we are ordering a box based on the key
                    amount = float(boxes[i].price) + amount # matching with the index the line and the right box
                    bought_l.append(Bought(boxes[i], 1.0)) # appending in the bought list
                elif to_order == key: # if true i have selected the product and check for quantity
                    if float(order_dict[quantity]) > products[i].quantity: # check for quantity
                        flash(products[i].name)
                        return redirect(url_for('farmer_store', id=id))
                    amount = float(products[i].price) * float(order_dict[quantity]) + amount # matching with the index the line and the right product
                    bought_l.append(Bought(products[i], order_dict[quantity]))

    if not bought_l: # if the consumer hasn't submitted anything i return an error
        flash('Error')
        return redirect(url_for('farmer_store', id=id))
    else:
        for element in bought_l:
            product = Product.query.filter_by(id=element.product.id).first()
            product.quantity = float(product.quantity) - float(element.quantity)
            db.session.commit()
    # storing info in the db
    # first creating the order, because we need the order id as a foreign key for order lines
    order_db = Order(consumer_id=session['id'],
                     supplier_id=id,
                     amount=amount,
                     date= datetime.utcnow(),
                     delivery_date=datetime.now() + timedelta(days=1))
    db.session.add(order_db)
    db.session.commit()

    order_id = Order.query.order_by(Order.id.desc()).first() # query for the last order inserted

    for element in bought_l: # using bought_l to store the info in the db of the bought product
        order_line = OrderLine(order_id=order_id.id,
                               product_id=element.product.id,
                               product_name=element.product.name,
                               supplier_id=id,
                               quantity=element.quantity,
                               partial_amount=float(element.product.price) * float(element.quantity))
        db.session.add(order_line)
        db.session.commit()

    return render_template('Pages/order_confirmation.html', bought=bought_l, amount=amount, supplier=supplier.supplier_name, order_id=order_id.id, title="Confirmed")

if __name__ == '__main__':
    app.run(debug=True)
