from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.fields.html5 import EmailField

from .models import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")

    def validate(self):
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors += ('Email not registered.', )
            return False
        return True

    def validate_username(self, email):
        if email.data != self.email:
            user = User.query.filter_by(username=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    register = SubmitField("Register")

    def validate(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors += ('Email already registered.', )
            return False
        return True
