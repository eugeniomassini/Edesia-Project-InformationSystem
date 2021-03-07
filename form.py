from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')


class consumerSignup_Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = StringField('Password', validators=[DataRequired(), Length(8, 20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)])
    submit = SubmitField('Register')