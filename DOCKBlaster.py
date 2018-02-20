import os
from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
import datetime
from dockblaster import helper
from flask_login import LoginManager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = helper.UPLOAD_FOLDER
now = datetime.datetime.now()

from dockblaster.database import db

login = LoginManager(app)

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', title="Home", heading="HOME")


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


if __name__ == '__main__':
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run()
