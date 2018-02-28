from flask import Blueprint, render_template, flash, redirect, request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from dockblaster import helper

blueprint = Blueprint('dock', __name__, url_prefix='/dock', static_folder='../static')


@blueprint.route('/docking_options', methods=['GET'])
def get_docking_options():
    return render_template("docking_options.html", title="Docking options", heading="Docking options")


@blueprint.route('/dock_integers', methods=['GET'])
def get_dock_integers():
    return render_template("dock_integers.html", title="Dock Integers", heading="Dock Integers")


@blueprint.route('/dock_strings', methods=['GET'])
def get_dock_strings():
    return render_template("dock_strings.html", title="Dock Strings", heading="Dock Strings")


@blueprint.route('/dock_list_of_strings', methods=['GET'])
def get_dock_list_of_strings():
    return render_template("dock_list_of_strings.html", title="Dock List of Strings", heading="Dock List of Strings")


@blueprint.route('/dock_files', methods=['GET'])
def get_dock_files():
    return render_template("dock_files.html", title="Dock files", heading ="Dock your files")


@blueprint.route('/submit_ligand_receptor_data', methods=['POST'])
def submit_ligand_receptor_data():
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
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename_a = secure_filename(file_a.filename)
        filename_b = secure_filename(file_b.filename)
        file_a.save(os.path.join(upload_folder, filename_a))
        file_b.save(os.path.join(upload_folder, filename_b))
        file_a_contents = helper.read_file_contents(upload_folder + str("/") + filename_a)
        file_b_contents = helper.read_file_contents(upload_folder + str("/") + filename_b)
        if helper.generate_result_file(file_a_contents, file_b_contents):
            user_id = current_user.get_id()
            return render_template("dock_results.html", title="DOCK Results", heading="DOCK Results")