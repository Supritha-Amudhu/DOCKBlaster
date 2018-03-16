from flask import Blueprint, render_template, flash, redirect, request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from dockblaster.database import db
import os, os.path
from dockblaster import helper
from dockblaster.helper import parse_file_name, parse_parameters_file
from .models import Docking_Job
import datetime

blueprint = Blueprint('dock', __name__, url_prefix='/dock', static_folder='../static')


@blueprint.route('/start', methods=['GET'])
def get_docking_options():
    job_types = parse_file_name(str(current_app.config['PARSE_FOLDER']))
    return render_template("docking_options.html", title="Docking options", heading="Docking options",
                           job_types=job_types)

@blueprint.route('/<job_type>', methods=['GET'])
def get_job_type(job_type):
    job_data = parse_parameters_file(str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/parameters.json")
    return render_template("dock_jobs.html", job_data=job_data)

@blueprint.route('/submit_docking_data/<job_type>', methods=['POST'])
def submit_docking_data(job_type):
    counter = 1
    job_data = parse_parameters_file(str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/parameters.json")
    user_id = current_user.get_id()
    date_started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    create_job_recipe = Docking_Job(user_id=user_id, job_status_id=1, date_started=date_started,
                                    job_type_id=job_data["job_number"],
                                    job_description=job_data["job_description"])
    db.session.add(create_job_recipe)
    db.session.flush()
    docking_job_id = create_job_recipe.docking_job_id
    db.session.commit()
    upload_folder = str(current_app.config['UPLOAD_FOLDER']) + str(docking_job_id % 10) + "/" + str(docking_job_id) + "/"
    helper.mkdir_p(upload_folder)
    for input in job_data["inputs"]:
        name = job_data['job_type_name'] + "_" + input['type'] + "_" + str(counter)
        counter = counter + 1
        if request.files.get(name):
            file = request.files[name]
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                file.save(os.path.join(upload_folder, input["file_name"]))
        elif request.form.get(name):
            file = request.form[name]
            if file == '':
                flash('Missing field values')
                return redirect(request.url)
            else:
                with open(upload_folder + input["file_name"], "wb") as fo:
                    fo.write(file)
                    fo.close()
    return render_template("dock_results.html", title="DOCK Results", heading="DOCK Results")

@blueprint.route('/dock_cluster', methods=['GET'])
def get_dock_cluster():
    return render_template("dock_cluster.html", title="Dock files", heading ="Dock your files")


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
    jobDescription = request.form['jobDescription']
    job_type_id = request.form['jobTypeID']
    job_type = request.form['jobTypeName']
    # if user does not select file, browser also
    # submit an empty part without filename
    if receptorFile.filename == '' or ligandFile.filename == '' or numberOfTries == '':
        flash('No selected file')
        return redirect(request.url)
    if (receptorFile and ligandFile and numberOfTries)\
            and helper.allowed_file(receptorFile.filename) and helper.allowed_file(ligandFile.filename) \
            and helper.allowed_file(expertFile.filename):

        user_id = current_user.get_id()
        date_started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        create_job_recipe = Docking_Job(user_id=user_id, job_status_id=1, date_started=date_started,
                                        job_type_id=job_type_id,
                                        job_description=jobDescription)
        db.session.add(create_job_recipe)
        db.session.flush()
        docking_job_id = create_job_recipe.docking_job_id
        db.session.commit()

        upload_folder = str(current_app.config['UPLOAD_FOLDER']) + job_type + "_" +\
                        str(docking_job_id) + "/"
        helper.mkdir_p(upload_folder)
        filename_receptor_file = 'receptor.txt'
        filename_ligand_file = 'xtal-lig.pdb'
        filename_expert_file = 'expert.tar'
        filename_number_of_tries = 'numberOfTries.txt'
        receptorFile.save(os.path.join(upload_folder, filename_receptor_file))
        ligandFile.save(os.path.join(upload_folder, filename_ligand_file))
        expertFile.save(os.path.join(upload_folder, filename_expert_file))
        receptorFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_receptor_file)
        ligandFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_ligand_file)
        expertFile_contents = helper.read_file_contents(upload_folder + str("/") + filename_expert_file)
        with open(upload_folder + filename_number_of_tries, "wb") as fo:
            fo.write(numberOfTries)
        if helper.generate_result_file(upload_folder, receptorFile_contents, ligandFile_contents, expertFile_contents):
            return render_template("dock_results.html", title="DOCK Results", heading="DOCK Results")