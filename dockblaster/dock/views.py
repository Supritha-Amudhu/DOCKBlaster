from flask import Blueprint, render_template, flash, redirect, request, current_app, url_for
from flask_login import current_user
from dockblaster.database import db
import os, os.path
from dockblaster.dock import helper
from dockblaster.dock.helper import parse_parameters_file, parse_parameters_file_recursive, parse_subfolders_for_folder
from .models import Docking_Job
import datetime
import subprocess
from subprocess import call
# from dockblaster.errors import errors_blueprint
# from dockblaster.errors import *



blueprint = Blueprint('dock', __name__, url_prefix='/', static_folder='../static')


@blueprint.route('error', methods=['GET'])
def display_error():
    return render_template("error_pages/page_not_found.html");


@blueprint.app_errorhandler(500)
@blueprint.errorhandler(500)
# @errors_blueprint.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error_pages/page_not_found.html'), 500


@blueprint.route('start', methods=['GET'])
def get_docking_options():
    job_data = parse_parameters_file_recursive(str(current_app.config['PARSE_FOLDER']))
    return render_template("dock_jobs/docking_options.html", title="Docking options", heading="Action?",
                           job_data=job_data, sub_heading_link_text = "How does this work?",
                           sub_heading_link = "http://wiki.docking.org/index.php/Blaster18")


@blueprint.route('start/<job_type>', methods=['GET'])
def get_job_type(job_type):
    job_data = parse_parameters_file(str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/parameters.json")
    return render_template("dock_jobs/dock_jobs.html", job_data=job_data, heading="Action: "+job_type, sub_heading=job_data["job_full_name"])


@blueprint.route('<job_type>/<docking_job_id>', methods=['GET'])
def docking_job_details(job_type, docking_job_id):
    folder_path_job_results = str(current_app.config['UPLOAD_FOLDER']) + str(int(docking_job_id) % 10) + "/" + str(job_type) + "_" + str(docking_job_id) + "/"
    files = parse_subfolders_for_folder(folder_path_job_results)
    file = open(folder_path_job_results+files[0])
    return render_template("docking_results/docking_job_results.html", title="DOCK Results", heading="DOCK Results", files=files, path=folder_path_job_results, input=file)


@blueprint.route('results/<job_type>', methods=['POST'])
def submit_docking_data(job_type):
    counter = 1
    job_data = parse_parameters_file(str(current_app.config['PARSE_FOLDER']) + str(job_type) + "/parameters.json")
    user_id = current_user.get_id()
    last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    memo = request.form.get("memo") or "No memo"
    create_job_recipe = Docking_Job(user_id=user_id,
                                    job_status_id=1,
                                    last_updated=last_updated,
                                    job_type_id=job_data["job_number"],
                                    memo=memo,
                                    marked_favorite= 0,
                                    deleted= False)
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
    return redirect(url_for('jobresults.get_folder_details', job_id = str(docking_job_id)))