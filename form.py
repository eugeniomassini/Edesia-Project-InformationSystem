from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from model import User

class login_Form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=16), DataRequired()])
    submit = SubmitField('Login')


class consumerSignup_Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = StringField('Password', validators=[DataRequired(), Length(8, 20)])
    address = StringField('Address')
    phone = StringField('Phone', validators=[DataRequired(), Length(min=7, max=12)])
    submit = SubmitField('Register')

    # Check if the email has already been registered
    def validate_email(self, email):
        user_check = User.query.filter_by(username=self.email.data).first()
        if user_check:
            raise ValidationError('This email has been register before')
