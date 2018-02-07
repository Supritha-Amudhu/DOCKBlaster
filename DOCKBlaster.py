from flask import Flask, render_template, redirect, request, url_for, request, flash
from config import Config
from login_form import LoginForm
import database

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title="Home", heading="HOME")


@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect("index.html")
    else:
        return render_template("login.html", title="Login", heading ="LOGIN", form=login_form)
    endif


@app.route('/dock_files', methods=['GET'])
def dock_files():
    return render_template("dock_files.html", title="Dock files", heading = "Dock your files")


if __name__ == '__main__':
    app.run()
