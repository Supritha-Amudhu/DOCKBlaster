# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, flash, current_app, request, json, jsonify
from flask_login import current_user
from dockblaster.dock.helper import parse_subfolders_find_folder_name
from dockblaster.job_results.helper import render_job_details, render_job_folder_details, delete_listed_jobs
from dockblaster.constants import JOB_STATUSES
from dockblaster.dock.models import Docking_Job

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


# Route that maps to the index os search results table
@blueprint.route('/', methods=['GET'])
@blueprint.route('/all/', methods=['GET'])
@blueprint.route('/all', methods=['GET'])
def render_job_list():
    if current_user.is_authenticated:
        return render_job_details(path='', results_table=True, status='', admin = current_user.is_admin())


# Route to delete jobs
@blueprint.route('/delete_jobs', methods=['DELETE'])
def delete_jobs():
    if current_user.is_authenticated:
        delete_jobs = request.get_json()
        delete_status = delete_listed_jobs(delete_jobs)
        delete_status = json.dumps(delete_status)
        delete_status = json.loads(delete_status)
        return jsonify(delete_status)


# Route to filter job results
@blueprint.route('/<path:filter>', methods=['GET'])
def filter_by_status(filter):
    if filter.capitalize().replace("_", " ") in JOB_STATUSES.values():
        return render_job_details(path='', results_table=True, status=filter.capitalize().replace("_", " "),
                                  admin = current_user.is_admin())
    else:
        flash("Invalid filter.", category='danger')
        return render_template("docking_results/docking_job_results.html", title="DOCK Results", path=filter, errors=True)


# Route to navigate to directories and subdirectories within job results
@blueprint.route('/<int:job_id>/<path:file>', methods=['GET'])
def read_download_job_files(job_id, file):
    # Check if the job path is a valid one, if not throw an error to the user
    admin = current_user.is_admin()
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), job_id) + "/" + file
    url_path = str(job_id) + "/" + file
    valid_job = Docking_Job.query.filter_by(docking_job_id=job_id).first()
    if admin or (current_user.is_authenticated and valid_job and \
            (int(current_user.get_id())) == valid_job.user_id):
        return render_job_folder_details(path, url_path, 1, admin)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_results/docking_job_results.html", title="DOCK Results", path=job_id, errors=True)


# Route that displays every job in detail
@blueprint.route('/<int:job_id>', methods=['GET'])
def get_folder_details(job_id):
    admin = current_user.is_admin()
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), job_id)
    valid_job = Docking_Job.query.filter_by(docking_job_id=job_id).first()
    if admin or (current_user.is_authenticated and valid_job and\
            (int(current_user.get_id())) == valid_job.user_id):
        return render_job_folder_details(path, job_id, 0, admin)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_results/docking_job_results.html", title="DOCK Results", path=path, errors=True)


