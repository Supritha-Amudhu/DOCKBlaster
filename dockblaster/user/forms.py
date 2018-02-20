from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

from .models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")

    def validate(self):
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Email not registered.')
            return False
        return True


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    register = SubmitField("Register")

    def validate(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered.')
            return False
        return True
