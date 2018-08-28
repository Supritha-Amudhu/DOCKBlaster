from hashlib import md5

import datetime

from flask import flash, redirect, url_for

from dockblaster.database import db
from dockblaster.user.models import User


def validate_and_save_user(request):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    email = request.form['email']
    date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    api_key = generate_api_key(password)
    if first_name == '' or last_name == '' or password == '' or email == '':
        flash("Please fill the required fields")
        return redirect(url_for('user.get_signup'))
    create_user_recipe = User(first_name=first_name, last_name=last_name, password=password, email=email,
                              date_created=date_created, api_key=api_key)
    db.session.add(create_user_recipe)
    db.session.commit()
    flash("Registration successful.", category='success')


def generate_api_key(password):
    api_key = md5(password).hexdigest()
    return api_key
