from flask import Flask, render_template, redirect, request, url_for, request, flash
from config import Config
from login_form import LoginForm
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

# from DOCKBlaster import routes, models

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title="Home", heading="HOME")


@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    recipe1 = User(1, 'supritha', 'soup@ucsf.edu', 'pwd')
    db.session.add(recipe1)
    db.session.commit()
    user = User.query.get(1)
    user.password_hash = 'mynewpassword'
    db.session.commit()
    if login_form.validate_on_submit():
        return redirect("index.html")
    else:
        return render_template("login.html", title="Login", heading ="LOGIN", form=login_form)
    endif


@app.route('/dock_files', methods=['GET'])
def dock_files():
    return render_template("dock_files.html", title="Dock files", heading = "Dock your files")


if __name__ == '__main__':
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run()
