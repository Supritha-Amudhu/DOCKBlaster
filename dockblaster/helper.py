import errno
import os
from os import listdir
from os.path import join, isdir
import json

ALLOWED_EXTENSIONS = set(['txt', 'pdb', 'tar'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file_contents(file):
    try:
        with open(file, "r") as f:
            content = f.read()
            return content
    finally:
        f.close()


def generate_result_file(upload_folder, receptorFile_contents, ligandFile_contents, expertFile_contents):
    try:
        with open(str(upload_folder) + "/output.txt", "wb") as fo:
            fo.write(receptorFile_contents + "\n" + ligandFile_contents + "\n" + expertFile_contents)
            return 1
    finally:
        fo.close()

def parse_parameters_file(path_to_file):
    data = json.load(open(path_to_file))
    return data

def parse_parameters_file_recursive(path_to_file):
    job_data = []
    for files in os.walk(path_to_file, topdown=True, onerror=None, followlinks=False):
        for file in files[2]:
            if file == "parameters.json":
                parameters_file_path = os.path.join(files[0], file)
                individual_job_data = read_file_contents(parameters_file_path)
                individual_job_data = json.loads(individual_job_data)
                # print individual_job_data["job_type_name"]
                job_data.append(individual_job_data)
                # job_data[individual_job_data["job_type_name"]] = individual_job_data
                # print job_data
    return job_data


def parse_file_name(path_to_file):
    job_types = [f for f in listdir(path_to_file) if isdir(join(path_to_file, f))]
    return job_types


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


