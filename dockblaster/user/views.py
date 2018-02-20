# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm, SignUpForm
from .models import User
from dockblaster.database import db
import datetime

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

@blueprint.route('/login', methods=['GET'])
def get_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect("index.html")
    return render_template("login.html", title="Login", heading ="LOGIN", form=login_form)


@blueprint.route('/login', methods=['POST'])
def on_login_submit():
    if current_user.is_authenticated:
        return render_template('index.html', title="Home", heading="HOME")
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid Email or Password")
            return render_template("login.html", title="Login", heading="LOGIN", form=login_form)
        login_user(user, remember=login_form.remember_me.data)
        return render_template('index.html', title="Home", heading="HOME")
    # return render_template("login.html", title="Login", heading="LOGIN", form=login_form)
    return redirect("login.html")

@blueprint.route('/logout', methods=['POST'])
def on_logout():
    logout_user()
    login_form = LoginForm()
    return render_template("login.html", title="Login", heading="LOGIN", form=login_form)


@blueprint.route('/sign_up', methods=['GET'])
def get_signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        return redirect("index.html")
    else:
        return render_template("sign_up.html", title="Sign Up", heading="Sign Up", form=sign_up_form)

@blueprint.route('/sign_up', methods=['POST'])
def on_submit_signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    email = request.form['email']
    date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    create_user_recipe = User(first_name=first_name, last_name=last_name, password=password, email=email,
                              date_created=date_created)
    db.session.add(create_user_recipe)
    db.session.commit()
    login_form = LoginForm()
    return render_template("login.html", title="Login", heading="LOGIN", form=login_form)