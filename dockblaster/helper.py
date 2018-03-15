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
    with open(file, "r") as f:
        content = f.read()
        return content


def generate_result_file(upload_folder, receptorFile_contents, ligandFile_contents, expertFile_contents):
    try:
        with open(str(upload_folder) + "/output.txt", "wb") as fo:
            fo.write(receptorFile_contents + "\n" + ligandFile_contents + "\n" + expertFile_contents)
            return 1
    finally:
        fo.close()

def parse_parameters_file(path_to_file):
    # try:
        data = json.load(open(path_to_file))
        print data
        job_parameters = {}
        return data
        # with open(path_to_file, 'r') as f:
        #     job_parameters = {}
        #     lines = f.readlines()
        #     # print lines
        #     lines = iter(lines)
        #     for line in lines:
        #         if(line == "jobtypename:\n"):
        #             job_parameters["jobtypename"] = next(lines).replace("\n", "")
        #         if(line == "fullname:\n"):
        #             job_parameters["fullname"] = next(lines).replace("\n", "")
        #     print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        #     print job_parameters
        #     return job_parameters
    # finally:
        # f.close()

# def write_to_text_file(file, path_to_file):
#


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


