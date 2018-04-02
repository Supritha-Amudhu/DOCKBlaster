# -*- coding: utf-8 -*-
"""File Explorer views."""

from flask import Blueprint, render_template, redirect, request, flash, current_app
from flask_login import current_user
import os
import os.path
from dockblaster.dock.models import Docking_Job
from dockblaster.job_results.helper import get_parent_job_folder
from dockblaster.helper import parse_subfolders_find_folder_name

blueprint = Blueprint('jobresults', __name__, url_prefix='/results', static_folder='../static')


@blueprint.route('/', methods=['GET'])
def render_job_list():
    return render_job_details(path='')


@blueprint.route('/<path:path>')
def get_folder_details(path):
    path = parse_subfolders_find_folder_name(str(current_app.config['UPLOAD_FOLDER']), path)
    if current_user.is_authenticated:
            return render_job_folder_details(path)
    else:
        flash("Job not found.", category='danger')
        return render_template("file_explorer.html", title="DOCK Results", heading="DOCK Results", path=path)

def render_job_details(path):
    user_jobs = Docking_Job.query.filter_by(user_id=current_user.get_id()).all()
    job_names = list()
    for user_job in user_jobs:
        parent_job_folder = user_job.docking_job_id % 10
        folder_path = str(current_app.config['UPLOAD_FOLDER'])+ "/" + str(parent_job_folder)
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            for dirname in dirnames:
                if dirname.endswith("_"+str(user_job.docking_job_id)):
                    job_names.append(dirname)
                    break
            break
    return render_template("file_explorer.html", title="DOCK Results", heading="DOCK Results",
                           dirs=job_names, path=path, previous_path = "-")


def render_job_folder_details(path):
    parent_docking_folder = get_parent_job_folder(path)
    requested_path = str(current_app.config['UPLOAD_FOLDER']) + "/" + str(parent_docking_folder) + "/" + path
    path_folders = path.split("/")
    del path_folders[len(path_folders) - 1]
    previous_path = "/".join(path_folders)
    if (parent_docking_folder != -1 and os.path.exists(requested_path)):
        if (os.path.isfile(requested_path)):
            with open(requested_path, 'r') as myfile:
                return myfile.read()
        else:
            for dirpath, dirnames, filenames in os.walk(str(requested_path)):
                return render_template("file_explorer.html", title="DOCK Results", heading="DOCK Results",
                                       files=filenames, dirs=dirnames, path=path, previous_path = previous_path)
    else:
        flash("The path you asked for does not exist.", category='danger')
        return render_template("file_explorer.html", title="DOCK Results", heading="DOCK Results",
                               path=path)
