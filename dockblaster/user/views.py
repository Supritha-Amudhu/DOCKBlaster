# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user, login_user, logout_user

from dockblaster.user.helper import validate_and_save_user
from .forms import LoginForm, SignUpForm
from .models import User
from dockblaster.database import db
import datetime

blueprint = Blueprint('user', __name__, url_prefix='/', static_folder='../static')


@blueprint.route('login', methods=['GET'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('public.index'))
    return render_template("user/login.html", title="Login", heading ="LOGIN", login_form=login_form)


@blueprint.route('login', methods=['POST'])
def on_login_submit():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Invalid Email or Password", category='danger')
            return render_template("user/login.html", title="Login", heading="LOGIN", login_form=login_form)
        login_user(user, remember=login_form.remember_me.data)
        flash("Logged in successfully", category='success')
        return redirect(url_for('public.index'))
    return render_template("user/login.html", title="Login", heading="LOGIN", login_form=login_form)


@blueprint.route('logout', methods=['GET','POST'])
def on_logout():
    logout_user()
    flash("Logged out successfully", category='success')
    return redirect('login')


@blueprint.route('sign_up', methods=['GET'])
def get_signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        return redirect(url_for('public.index'))
    else:
        return render_template("user/sign_up.html", title="Sign Up", heading="Sign Up", form=sign_up_form)


@blueprint.route('sign_up', methods=['POST'])
def on_submit_signup():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        validate_and_save_user(request)
        return redirect(url_for('user.get_login'))
    flash("Sign up unsuccessful. Please sign up again.", category='danger')
    return redirect(url_for('user.get_signup'))
