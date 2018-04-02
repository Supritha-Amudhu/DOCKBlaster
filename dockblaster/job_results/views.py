# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, redirect, request, flash, current_app
from flask_login import current_user
from dockblaster.helper import parse_subfolders_find_folder_name
from dockblaster.job_results.helper import render_job_details, render_job_folder_details

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def render_job_list():
    if current_user.is_authenticated:
        return render_job_details(path='')


@blueprint.route('/<path:path>')
def get_folder_details(path):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), path)
    if current_user.is_authenticated:
            return render_job_folder_details(path)
    else:
        flash("Job not found.", category='danger')
        return render_template("file_explorer.html", title="DOCK Results", heading="DOCK Results", path=path)

