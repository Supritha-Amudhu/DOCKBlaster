from dockblaster.dock.models import Docking_Job, Job_Status
from flask import render_template, flash, current_app
from flask_login import current_user
import os
import os.path
from dockblaster.database import db

# This method will get the parent folder for every job. Ex - cluster_57 is the job, the parent folder under Jobs is 7
def get_parent_job_folder(path):
    docking_job_folder = path.split("/")[0]
    if docking_job_folder:
        if len(docking_job_folder.split("_")) == 2:
            docking_job_id = docking_job_folder.split("_")[1]
            if docking_job_id:
                return int(docking_job_id) % 10
    return -1


# A helper method that retrieves all the jobs created by the current user
def get_active_jobs_current_user():
    job_data = Docking_Job.query.join(Job_Status, Docking_Job.job_status_id == Job_Status.job_status_id) \
            .add_columns(Docking_Job.docking_job_id, Docking_Job.job_status_id, Docking_Job.memo,
                         Docking_Job.last_updated,
                         Docking_Job.user_id, Job_Status.job_status_name).\
                        filter(Docking_Job.user_id == current_user.get_id()).filter(Docking_Job.deleted == False)
    return job_data


def render_job_details(path, results_table, status):
    if status == 'All' or status == '':
        job_data = get_active_jobs_current_user()
    else:
        job_data = get_active_jobs_current_user().filter(
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
                    # job_names[dirname]['status'] = user_job.job_status
                    job_names[dirname]['memo'] = user_job.memo
                    job_names[dirname]['last_updated'] = user_job.last_updated
                    break
            break
    if results_table:
        return render_template("docking_job_results_table.html", title="DOCK Results List",
                               dirs=job_names, path='', previous_path="back_button")
    else:
        return render_template("docking_job_results.html", title="DOCK Results",
                               dirs=job_names, path=path, previous_path = "back_button")


def render_job_folder_details(path, job_id):
    job_information_grid = dict()
    job_data = get_active_jobs_current_user().filter(Docking_Job.docking_job_id == job_id).first()
    parent_docking_folder = get_parent_job_folder(path)
    requested_file_system_path = str(current_app.config['UPLOAD_FOLDER']) + str(parent_docking_folder) + "/" + path
    path_folders = str(job_id).split("/")
    job_information_grid['job_type'] = path.split("_")[0]
    del path_folders[len(path_folders) - 1]
    previous_path = "/".join(path_folders)
    job_information_grid['job_number'] = job_data.docking_job_id
    job_information_grid['job_status'] = job_data.job_status_name
    job_information_grid['memo'] = job_data.memo
    job_information_grid['last_updated'] = job_data.last_updated
    if (parent_docking_folder != -1 and os.path.exists(requested_file_system_path)):
        if (os.path.isfile(requested_file_system_path)):
            with open(requested_file_system_path, 'r') as my_file:
                return my_file.read()
        else:
            for dirpath, dirnames, filenames in os.walk(str(requested_file_system_path)):
                return render_template("docking_job_results.html", title="DOCK Results",
                                       files=filenames, dirs=dirnames, path=str(job_id), previous_path = previous_path,
                                       job_information_grid = job_information_grid, data_grid = True)
    else:
        flash("The path you asked for does not exist.", category='danger')
        return render_template("docking_job_results.html", title="DOCK Results",
                               path=path)


def delete_listed_jobs(jobs):
    delete_status = dict()
    for job_id in jobs:
        docking_job = Docking_Job.query.filter(Docking_Job.docking_job_id == int(job_id)).\
            filter(Docking_Job.user_id == current_user.get_id()).first()
        docking_job.update_deleted(True)
        db.session.commit()
        delete_status[str(job_id)] = docking_job.deleted
    return delete_status