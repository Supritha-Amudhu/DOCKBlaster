# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, flash, current_app
from flask_login import current_user
from dockblaster.dock.helper import parse_subfolders_find_folder_name
from dockblaster.job_results.helper import render_job_details, render_job_folder_details
from dockblaster.constants import JOB_STATUSES
from dockblaster.dock.models import Docking_Job

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/all', methods=['GET'])
def render_job_list():
    if current_user.is_authenticated:
        return render_job_details(path='', results_table=True, status='')


@blueprint.route('/<path:filter>', methods=['GET'])
def filter_by_status(filter):
    if current_user.is_authenticated and (int(current_user.get_id())) == \
            Docking_Job.query.filter_by(docking_job_id=filter).first().user_id:
        flash("The path you asked for does not exist.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results",
                               path=filter)
    if filter.capitalize().replace("_", " ") in JOB_STATUSES.values():
        return render_job_details(path='', results_table=True, status=filter.capitalize().replace("_", " "))


@blueprint.route('/<int:job_id>/<path:file>', methods=['GET'])
def read_download_job_files(job_id, file):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), job_id) + "/" + file
    url_path = str(job_id) + "/" + file
    if current_user.is_authenticated and (int(current_user.get_id())) == \
            Docking_Job.query.filter_by(docking_job_id=job_id).first().user_id:
        return render_job_folder_details(path, url_path)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results", path=job_id)


@blueprint.route('/<int:job_id>', methods=['GET'])
def get_folder_details(job_id):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), job_id)
    if current_user.is_authenticated and (int(current_user.get_id())) == \
            Docking_Job.query.filter_by(docking_job_id = job_id).first().user_id:
        return render_job_folder_details(path, job_id)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results", path=path)


