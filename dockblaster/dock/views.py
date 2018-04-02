from flask import Blueprint, render_template, flash, redirect, request, current_app, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from dockblaster.database import db
import os, os.path
from dockblaster import helper
from dockblaster.helper import parse_parameters_file, parse_parameters_file_recursive, parse_subfolders_for_folder
from .models import Docking_Job
import datetime
import subprocess
from subprocess import call

blueprint = Blueprint('dock', __name__, url_prefix='/dock', static_folder='../static')


@blueprint.route('/start', methods=['GET'])
def get_docking_options():
    job_data = parse_parameters_file_recursive(str(current_app.config['PARSE_FOLDER']))
    return render_template("docking_options.html", title="Docking options", heading="What do you want?",
                           job_data=job_data)


@blueprint.route('/<job_type>', methods=['GET'])
def get_job_type(job_type):
    job_data = parse_parameters_file(str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/parameters.json")
    return render_template("dock_jobs.html", job_data=job_data, heading="Action: "+job_type, sub_heading=job_data["job_full_name"])


# @blueprint.route('/<job_type>/<job_ID>', defaults={'job_data': None})
@blueprint.route('/<job_type>/<docking_job_id>', methods=['GET'])
def docking_job_details(job_type, docking_job_id):
    folder_path_job_results = str(current_app.config['UPLOAD_FOLDER']) + str(int(docking_job_id) % 10) + "/" + str(job_type) + "_" + str(docking_job_id) + "/"
    files = parse_subfolders_for_folder(folder_path_job_results)
    file = open(folder_path_job_results+files[0])
    # print ">>>>>>>>>>>"
    # print file
    return render_template("docking_results_job_details.html", title="DOCK Results", heading="DOCK Results", files=files, path=folder_path_job_results, input=file)


@blueprint.route('/results/<job_type>', methods=['POST'])
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
    upload_folder = str(current_app.config['UPLOAD_FOLDER']) + str(docking_job_id % 10) + "/" + job_type + "_" + str(docking_job_id) + "/"
    helper.mkdir_p(upload_folder)
    for input in job_data["inputs"]:
        name = job_data['job_type_name'] + "_" + input['type'] + "_" + str(counter)
        counter = counter + 1
        if request.files.get(name):
            file = request.files.get(name)
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                file.save(os.path.join(upload_folder, input["file_name"]))
        elif request.form.get(name):
            if input["type"] == "check_box":
                file = request.form.getlist(name)
                file = ", ".join(file)
            else:
                file = request.form.get(name)
            if file == '':
                flash('Missing field values')
                return redirect(request.url)
            else:
                with open(upload_folder + input["file_name"], "wb") as fo:
                    fo.write(file)
                    fo.close()
    path = str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/" + job_data["command"]
    qsub = "qsub " + path + " " + upload_folder + " > jobID"
    if job_data["batchq"] == "0":
        subprocess.call([path, upload_folder])
    else:
        os.chdir(upload_folder)
        out = subprocess.Popen(qsub, shell=True)
        out.communicate()[0]
    with open(upload_folder + job_data["job_output"], "w") as fo:
        fo.write(str(""))
        fo.close()
    return redirect(url_for('dock.docking_job_details', job_type=job_type,job_ID=docking_job_id))
