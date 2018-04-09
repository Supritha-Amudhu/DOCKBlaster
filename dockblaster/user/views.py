# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm, SignUpForm
from .models import User
from dockblaster.database import db
import datetime

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/login', methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('public.index'))
    return render_template("login.html", title="Login", heading ="LOGIN", login_form=login_form)


@blueprint.route('/login', methods=['POST'])
def on_login_submit():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid Email or Password", category='danger')
            return render_template("login.html", title="Login", heading="LOGIN", login_form=login_form)
        login_user(user, remember=login_form.remember_me.data)
        flash("Logged in successfully", category='success')
        return redirect(url_for('public.index'))
    return render_template("login.html", title="Login", heading="LOGIN", login_form=login_form)


@blueprint.route('/logout', methods=['GET','POST'])
def on_logout():
    logout_user()
    flash("Logged out successfully", category='success')
    return redirect('users/login')


@blueprint.route('/sign_up', methods=['GET'])
def get_signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        return redirect(url_for('public.index'))
    else:
        return render_template("sign_up.html", title="Sign Up", heading="Sign Up", form=sign_up_form)


@blueprint.route('/sign_up', methods=['POST'])
def on_submit_signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email = request.form['email']
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if first_name == '' or last_name == '' or password == '' or email == '':
            flash("Please fill the required fields")
            return redirect(url_for('user.get_signup'))
        create_user_recipe = User(first_name=first_name, last_name=last_name, password=password, email=email,
                                  date_created=date_created)
        db.session.add(create_user_recipe)
        db.session.commit()
        flash("Registration successful.", category='success')
        return redirect(url_for('user.get_login'))
    flash("Sign up unsuccessful. Please sign up again.", category='danger')
    return redirect(url_for('user.get_signup'))
