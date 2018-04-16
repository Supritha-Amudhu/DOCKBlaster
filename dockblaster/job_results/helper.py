from dockblaster.dock.models import Docking_Job, Job_Status
from flask import render_template, flash, current_app
from flask_login import current_user
import os
import os.path
from dockblaster.database import db


def get_parent_job_folder(path):
    docking_job_folder = path.split("/")[0]
    if docking_job_folder:
        if len(docking_job_folder.split("_")) == 2:
            docking_job_id = docking_job_folder.split("_")[1]
            if docking_job_id:
                return int(docking_job_id) % 10
    return -1


def render_job_details(path, results_table, status):
    if status == 'All' or status == '':
        job_data = Docking_Job.query.join(Job_Status, Docking_Job.job_status_id == Job_Status.job_status_id) \
            .add_columns(Docking_Job.docking_job_id, Docking_Job.job_status_id, Docking_Job.memo,
                         Docking_Job.date_started,
                         Docking_Job.user_id, Job_Status.job_status_name).filter(Docking_Job.user_id == current_user.get_id())
    else:
        job_data = Docking_Job.query.join(Job_Status, Docking_Job.job_status_id == Job_Status.job_status_id)\
            .add_columns(Docking_Job.docking_job_id, Docking_Job.job_status_id, Docking_Job.memo,
                         Docking_Job.date_started,
                         Docking_Job.user_id, Job_Status.job_status_name).filter\
                        (Docking_Job.user_id == current_user.get_id(),
                         Job_Status.job_status_name.like("%" + str(status) + "%"))
    job_names = dict()
    for user_job in job_data:
        parent_job_folder = user_job.docking_job_id % 10
        folder_path = str(current_app.config['UPLOAD_FOLDER']) + str(parent_job_folder)
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            for dirname in dirnames:
                if dirname.endswith("_"+str(user_job.docking_job_id)):
                    job_names[dirname] = dict()
                    job_names[dirname]['job_type'] = dirname.split("_")[0]
                    job_names[dirname]['status'] = user_job.job_status_name
                    job_names[dirname]['memo'] = user_job.memo
                    job_names[dirname]['date_submitted'] = user_job.date_started
                    break
            break
    if results_table:
        return render_template("docking_job_results_table.html", title="DOCK Results List", heading="DOCK Results List",
                               dirs=job_names, path='', previous_path="back_button")
    else:
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results",
                               dirs=job_names, path=path, previous_path = "back_button")


def render_job_folder_details(path, job_id):
    parent_docking_folder = get_parent_job_folder(path)
    requested_file_system_path = str(current_app.config['UPLOAD_FOLDER']) + str(parent_docking_folder) + "/" + path
    path_folders = str(job_id).split("/")
    del path_folders[len(path_folders) - 1]
    previous_path = "/".join(path_folders)
    if (parent_docking_folder != -1 and os.path.exists(requested_file_system_path)):
        if (os.path.isfile(requested_file_system_path)):
            with open(requested_file_system_path, 'r') as my_file:
                return my_file.read()
        else:
            for dirpath, dirnames, filenames in os.walk(str(requested_file_system_path)):
                return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results",
                                       files=filenames, dirs=dirnames, path=str(job_id), previous_path = previous_path)
    else:
        flash("The path you asked for does not exist.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results", heading="DOCK Results",
                               path=path)
