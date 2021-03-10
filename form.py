from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from model import *

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')

# Registration form for the consuemer
class ConsumerRegForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    address = StringField('Address', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)]) #TODO find a phone validator. number
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')

    # Function to validate email
    # if the query is false raises error
    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('This user has been register before or taken')
