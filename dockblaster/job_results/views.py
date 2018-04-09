# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, flash, current_app
from flask_login import current_user
from dockblaster.dock.helper import parse_subfolders_find_folder_name
from dockblaster.job_results.helper import render_job_details, render_job_folder_details
from dockblaster.constants import JOB_STATUSES

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def render_job_list():
    if current_user.is_authenticated:
        return render_job_details(path='', results_table=True, status='')


@blueprint.route('/<path:path>', methods=['GET'])
def get_folder_details(path):
    if path in JOB_STATUSES:
        return render_job_details(path='', results_table=False, status='')
    else:
        path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), path)
        if current_user.is_authenticated:
                return render_job_folder_details(path)
        else:
            flash("Job not found.", category='danger')
            return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results", path=path)

