from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import email_validator
from model import User, Consumer, Supplier, Review, ShoppingCart, Order, OrderLines, Message


class ConsumerRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    familyname = StringField('Family Name', validators=[DataRequired(), Length(min=3, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)]) #TODO find a phone validator. number
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user_check = User.query.filter_by(email=self.email.data).first()
        if user_check:
            raise ValidationError('This user has been register before or taken')


class SupplierRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    piva = StringField('piva', validators=[DataRequired(), Length(min=3, max=25)]) # TODO PIVA validator. number. code
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)])  # TODO find a phone validator. number
    description = StringField('Description', validators=[DataRequired(), Length(max=500)]) # no minimum and max of 500 characters
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')


class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=3, max=15), DataRequired()])
    submit = SubmitField('Login')