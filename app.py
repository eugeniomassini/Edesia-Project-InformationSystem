# TODO import things I'll need
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_bcrypt import Bcrypt
import os
from flask_mail import Mail, Message

app = Flask(__name__)


app.config['GMAPS_API']=os.environ.get('GMAPS_API')

# Database configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# login_manager.init_app(app)

from model import *
from form import *

def send_mail(to, subject, **kwargs):
    msg = Message(subject,
                  sender = app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template('welcome-mail.html', **kwargs)
    mail.send(msg)

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


    order1 = Order(consumer_id=1,
                   supplier_id=2,
                   amount=15.00)
    db.session.add(order1)
    db.session.commit()
    orderline1 = OrderLine(order_id=1,
                           supplier_id=2,
                           product_id=2,
                           product_name='Beats',
                           quantity=3.00,
                           partial_amount=9.00)
    db.session.add(orderline1)
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
# TODO google maps search bar
@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    session['GMAPS_API']=app.config['GMAPS_API']
    researchForm = ResearchForm()
    if researchForm.validate_on_submit():
        return redirect(url_for('research', city=researchForm.city.data))
    return render_template("Pages/general/homepage.html", title="Homepage - Edesia", form=researchForm)

# About Us routing
@app.route('/about-us')
def about_us():
    return render_template("Pages/general/about-us.html", title="About Us - Edesia")

#Contact Us routing
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
            # send email
            send_mail(registrationForm.email.data,
                      'You have registered successfully',
                      name=registrationForm.name.data,
                      username=registrationForm.email.data,
                      password=registrationForm.password.data)
            return redirect(url_for('login'))
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
            city = str(registrationForm.address.data)
            address = city.split(',')
            if any(str.isdigit(c) for c in address[1]):
                to_remove = address[0] + ',' + address[1] + ', '
            else:
                to_remove = address[0] + ', '

            city = city.replace(to_remove, '')
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
            session['roleid']=user.roleid
            session['id']=user.id
            if user.roleid == 2:
                return redirect(url_for('consumer', id=user.id))
            elif user.roleid == 1:
                return redirect(url_for('supplier', id=user.id, page='orders'))
    return render_template('Pages/login.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

# Consumer profile page
@app.route('/consumer/<int:id>')
@login_required
def consumer(id):
    consumer = Consumer.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    orders = Order.query.filter_by(consumer_id=id).order_by(Order.id.desc()).all()
    l_order_cons =[]

    class OrderCons():
        def __init__(self, order, content):
            self.order = order
            self.content = content


    for o in orders:
        products = []
        lines = OrderLine.query.filter_by(order_id=o.id)

        for l in lines:
            products.append(l)

        l_order_cons.append(OrderCons(o, products))

    return render_template('Pages/profile/profile_consumer-orders.html', consumer=consumer, user=user, orders=l_order_cons)

@app.route('/consumer/<int:id>/review/order_id=<int:order_id>', methods=['GET', 'POST'])
@login_required
def consumer_review(id, order_id):
    consumer = Consumer.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    order = Order.query.filter_by(id=order_id).first()

    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(order_id=order.id,
                        consumer_id=id,
                        supplier_id=order.supplier_id,
                        text= form.text.data)
        order.review=True
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('consumer', id=id))

    return render_template('Pages/profile/profile_consumer-review.html', consumer=consumer, user=user, form=form, order=order)

# Supplier page
@app.route('/supplier/<int:id>/<page>', methods=['GET', 'POST'])
@login_required
def supplier(id, page):
    supplier = Supplier.query.filter_by(id=id).first()
    user = User.query.filter_by(id=id).first()
    if page == "orders":
        orders = Order.query.filter_by(supplier_id=id).all()
        l_order_cons = []

        class OrderCons():
            def __init__(self, order, content):
                self.order = order
                self.content = content

        for o in orders:
            products = []
            lines = OrderLine.query.filter_by(order_id=o.id)

            for l in lines:
                products.append(l)

            l_order_cons.append(OrderCons(o, products))
        return render_template('Pages/profile/profile_supplier-orders.html', supplier=supplier, user=user, orders=l_order_cons)
    elif page == "products":
        products = Product.query.filter_by(supplier_id=id).all()
        return render_template('Pages/profile/profile_supplier-products.html', supplier=supplier, user=user, products=products)
    elif page == "add-product":
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(supplier_id=id,
                              price=form.price.data,
                              name=form.name.data,
                              quantity=form.quantity.data,
                              box=False)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('supplier', id=id, page='products'))
        return render_template('Pages/profile/profile-supplier_addProduct.html', supplier=supplier, user=user, form=form)
    elif page == "add-box":
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(supplier_id=id,
                              price=form.price.data,
                              description=form.description.data,
                              name=form.name.data,
                              quantity=form.quantity.data,
                              box=True)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('supplier', id=user.id, page='products'))
        return render_template('Pages/profile/profile-supplier_addBox.html', supplier=supplier, user=user, form=form)

@app.route('/supplier/<int:id>/edit-product=<int:product_id>', methods=['GET', 'POST'])
@login_required
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

    form.name.data = product.name
    form.quantity.data = product.quantity
    form.price.data = product.price
    form.description.data = product.description

    return render_template('Pages/profile/profile_supplier-edit_products.html', supplier=supplier, user=user, form=form, products=products, product_id=product_id)


# 3 Ordering process
# Research, Farmer store, place order

# 1 Step: Research
@app.route('/research/<city>')
def research(city):
    suppliers = Supplier.query.filter_by(supplier_city=city).all()
    return render_template("Pages/research_result.html", suppliers=suppliers)

# 2 Step: Display Farmer Store
# Pass the id the farmer to show his page
@app.route('/farmer_store/<int:id>', methods=['GET', 'POST'])
def farmer_store(id):
    supplier = Supplier.query.filter_by(id=id).first()
    products = Product.query.filter(Product.supplier_id==id, Product.box==False, Product.quantity>0.0).all()
    boxes = Product.query.filter(Product.supplier_id==id, Product.box==True, Product.quantity>0.0).all()
    min_entries = len(products)+len(boxes)
    class LocalForm(OrderForm):pass
    LocalForm.order = FieldList(FormField(OrderEntryForm), min_entries=min_entries)
    form=LocalForm()

    reviews = Review.query.filter_by(supplier_id=id).all()

    return render_template("Pages/farmer_store.html", supplier=supplier, products=products, boxes=boxes, form=form, reviews=reviews)

# 3 Step: Elaborate and Validate the order
@app.route('/order/confirmation/<int:id>', methods=['POST'])
@login_required
def order_func(id):
    if session['roleid'] == 1:
        return redirect(url_for('homepage'))

    supplier = Supplier.query.filter_by(id=id).first()
    products = Product.query.filter_by(supplier_id=id, box=False).all()
    boxes = Product.query.filter_by(supplier_id=id, box=True).all()
    n = len(products)+len(boxes)
    order = request.form
    order_dict = { x:order[x] for x in order if "order-" in x}
    amount = 0.0
    bought_l = []
    class Bought():
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity

    for i in range(n):
        str = 'order-%d' % i
        for key in order_dict.iterkeys():
            if str in key:
                quantity = str + '-quantity'
                to_order = str + '-to_order'
                if 'box' in key:
                    amount = float(boxes[i].price) + amount
                    bought_l.append(Bought(boxes[i], 1.0))
                    print order_dict[key]
                elif to_order == key:
                    if float(order_dict[quantity]) > products[i].quantity:
                        flash(products[i].name)
                        return redirect(url_for('farmer_store', id=id))
                    amount = float(products[i].price) * float(order_dict[quantity]) + amount
                    bought_l.append(Bought(products[i], order_dict[quantity]))
                    print order_dict[key]

    if not bought_l:
        flash('Error')
        return redirect(url_for('farmer_store', id=id))
    else:
        for element in bought_l:
            product = Product.query.filter_by(id=element.product.id).first()
            product.quantity = float(product.quantity) - float(element.quantity)
            db.session.commit()

    order_db = Order(consumer_id=session['id'],
                     supplier_id=id,
                     amount=amount)
    db.session.add(order_db)
    db.session.commit()

    order_id = Order.query.order_by(Order.id.desc()).first()

    for element in bought_l:
        order_line = OrderLine(order_id=order_id.id,
                               product_id=element.product.id,
                               product_name=element.product.name,
                               supplier_id=id,
                               quantity=element.quantity,
                               partial_amount=float(element.product.price) * float(element.quantity))
        db.session.add(order_line)
        db.session.commit()

    return render_template('Pages/order_confirmation.html', bought=bought_l, amount=amount, supplier=supplier.supplier_name, order_id=order_id.id)

if __name__ == '__main__':
    app.run(debug=True)
