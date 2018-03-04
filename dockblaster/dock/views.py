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
    if ('receptorFile' and 'ligandFile' not in request.files) and ('numberOfTries' not in request.form):
        flash('Files to be uploaded missing.')
        return redirect(request.url)
    receptorFile = request.files['receptorFile']
    ligandFile = request.files['ligandFile']
    expertFile = request.files['expertFile'] or None
    numberOfTries = request.form['numberOfTries']
    # if user does not select file, browser also
    # submit a empty part without filename
    if receptorFile.filename == '' or ligandFile.filename == '' or numberOfTries == '':
        flash('No selected file')
        return redirect(request.url)
    if receptorFile and ligandFile and numberOfTries and helper.allowed_file(receptorFile.filename) and helper.allowed_file(ligandFile.filename) and helper.allowed_file(expertFile.filename):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        filename_receptorFile = 'receptor.txt'
        filename_ligandFile = 'xtal-lig.pdb'
        filename_expertFile = 'expert.tar'
        filename_numberOfTries = 'numberOfTries.txt'
        receptorFile.save(os.path.join(upload_folder, filename_receptorFile))
        ligandFile.save(os.path.join(upload_folder, filename_ligandFile))
        expertFile.save(os.path.join(upload_folder, filename_expertFile))
        receptorFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_receptorFile)
        ligandFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_ligandFile)
        expertFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_expertFile)
        with open("/Users/supritha/Workspace/PycharmProjects/DOCKBlaster/Files/"+filename_numberOfTries, "wb") as fo:
            fo.write(numberOfTries)
        if helper.generate_result_file(receptorFile_contents, ligandFile_contents, expertFile_contents):
            # user_id = current_user.get_id()
            return render_template("dock_results.html", title="DOCK Results", heading="DOCK Results")