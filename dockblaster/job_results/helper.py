def get_parent_job_folder(path):
    docking_job_folder = path.split("/")[0]
    if docking_job_folder:
        if len(docking_job_folder.split("_")) == 2:
            docking_job_id = docking_job_folder.split("_")[1]
            if docking_job_id:
                return int(docking_job_id) % 10
    return -1
