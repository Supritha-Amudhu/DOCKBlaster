from DOCKBlaster import app
import os
from flask import render_template, redirect, request, url_for, request, flash
import helper, datetime
from login_form import LoginForm, SignUpForm
from flask_login import  current_user, login_user
from werkzeug.utils import secure_filename
from models import db, User


# @app.config["UPLOAD_FOLDER"] = helper.UPLOAD_FOLDER
now = datetime.datetime.now()

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title="Home", heading="HOME")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        login_form = LoginForm()
        # recipe1 = User(1, 'supritha', 'soup@ucsf.edu', 'pwd')
        # db.session.add(recipe1)
        # db.session.commit()
        # user = User.query.get(1)
        # user.password_hash = 'mynewpassword'
        # db.session.commit()
        if login_form.validate_on_submit():
            return redirect("index.html")
        return render_template("login.html", title="Login", heading ="LOGIN", form=login_form)
    else:
        if current_user.is_authenticated:
            return render_template('index.html', title="Home", heading="HOME")
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user is None or not user.check_password(login_form.password.data):
                flash("Invalid Username or Password")
                return render_template("login.html", title="Login", heading="LOGIN", form=login_form)
            login_user(user, remember=login_form.remember_me.data)
            return render_template('index.html', title="Home", heading="HOME")
        return render_template("login.html", title="Login", heading="LOGIN", form=login_form)


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        sign_up_form = SignUpForm()
        if sign_up_form.validate_on_submit():
            return redirect("index.html")
        else:
            return render_template("sign_up.html", title="Sign Up", heading="Sign Up", form=sign_up_form)
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        date_created = now.strftime("%Y-%m-%d %H:%M")
        login_form = LoginForm()
        create_user_recipe = User(user_id = 1, username = username, password_hash = password, email = email,
                                  date_created = date_created)
        db.session.add(create_user_recipe)
        db.session.commit()
        return render_template("login.html", title="Login", heading="LOGIN", form=login_form)


@app.route('/dock_files', methods=['GET'])
def dock_files():
    return render_template("dock_files.html", title="Dock files", heading = "Dock your files")


@app.route('/submit_ligand_receptor_data', methods=['GET','POST'])
def submit_ligand_receptor_data():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file_a' and 'file_b' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_a = request.files['file_a']
        file_b = request.files['file_b']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file_a.filename == '' or file_b.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_a and file_b and helper.allowed_file(file_a.filename) and helper.allowed_file(file_b.filename):
            filename_a = secure_filename(file_a.filename)
            filename_b = secure_filename(file_b.filename)
            file_a.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_a))
            file_b.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_b))
            file_a_contents = helper.read_file_contents(app.config['UPLOAD_FOLDER'] + str("/") + filename_a)
            file_b_contents = helper.read_file_contents(app.config['UPLOAD_FOLDER'] + str("/") + filename_b)
            if helper.generate_result_file(file_a_contents, file_b_contents):
                return render_template("dock_results.html", title="DOCK Results", heading="DOCK Results")


# @app.route('/dock_results', methods=['GET','POST'])
# def dock_results():
