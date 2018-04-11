# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, flash, current_app
from flask_login import current_user
from dockblaster.dock.helper import parse_subfolders_find_folder_name
from dockblaster.job_results.helper import render_job_details, render_job_folder_details
from dockblaster.constants import JOB_STATUSES

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


@blueprint.route('/', methods=['GET'])
@blueprint.route('/all', methods=['GET'])
def render_job_list():
    if current_user.is_authenticated:
        return render_job_details(path='', results_table=True, status='')


@blueprint.route('/<path:filter>', methods=['GET'])
def filter_by_status(filter):
    if filter.capitalize().replace("_", " ") in JOB_STATUSES.values():
        return render_job_details(path='', results_table=True, status=filter.capitalize().replace("_", " "))


@blueprint.route('/<path:path>/<path:file>', methods=['GET'])
def read_download_job_files(path, file):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), path) + "/" + file
    if current_user.is_authenticated:
        return render_job_folder_details(path)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results", path=path)


@blueprint.route('/<int:path>', methods=['GET'])
def get_folder_details(path):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), path)
    if current_user.is_authenticated:
            return render_job_folder_details(path)
    else:
        flash("Job not found.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results", path=path)


