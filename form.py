from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from model import *
from markupsafe import Markup

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')

# Registration form for the consumer
class ConsumerRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)]) #TODO find a phone validator. number
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

    # Function to validate email
    # if the query is false raises error
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This user has been register before or taken')

# Registration form for the supplier
class SupplierRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    piva = StringField('PIVA', validators=[DataRequired(), Length(min=3, max=25)]) # TODO PIVA validator. number. code
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)])  # TODO find a phone validator. number
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)]) # no minimum and max of 500 characters
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This user has been register before or taken')

class ResearchForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Search')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=3, max=25)])
    quantity = FloatField('Quantity in kg', validators=[DataRequired()])
    price = FloatField('Price/kg', validators=[DataRequired()])
    description =TextAreaField('Description', validators=[Length(max=500)])
    submit = SubmitField('Add Product')

class OrderEntryForm(FlaskForm):
    name = StringField()
    quantity = FloatField('Quantity')
    price = FloatField()
    to_order = BooleanField('Add Product')

class OrderForm(FlaskForm):
    order = FieldList(FormField(OrderEntryForm))
    submit = SubmitField('Confirm Order')