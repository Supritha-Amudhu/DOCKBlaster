from dockblaster.dock.models import Docking_Job
from flask import render_template, flash, current_app
from flask_login import current_user
import os
import os.path


def get_parent_job_folder(path):
    docking_job_folder = path.split("/")[0]
    if docking_job_folder:
        if len(docking_job_folder.split("_")) == 2:
            docking_job_id = docking_job_folder.split("_")[1]
            if docking_job_id:
                return int(docking_job_id) % 10
    return -1


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
    requested_path = str(current_app.config['UPLOAD_FOLDER']) + str(parent_docking_folder) + "/" + path
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
