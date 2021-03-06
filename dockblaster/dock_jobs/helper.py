import errno
import os
from os import listdir
from os.path import join, isfile, isdir
import json
from operator import itemgetter

ALLOWED_EXTENSIONS = set(['txt', 'pdb', 'tar'])


"""
    Define filenames that are allowed to be uploaded
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
    Parse a give file and read its contents
"""
def read_file_contents(file):
    try:
        with open(file, "r") as f:
            content = f.read()
            return content
    except IOError as err:
        print("IO error: {0}".format(err))
    else:
        print "File read successfuly"
    finally:
        f.close()


"""
    Parse all the job type template folders to find the parameters.txt file for each job type
"""
def parse_parameters_file(path_to_file):
    try:
        data = json.load(open(path_to_file))
    except IOError as err:
        print("IO error: {0}".format(err))
        raise
    else:
        print "Parameters file parsed successfully"
    return data


"""
    Parse all the job type template folders to find the parameters.txt file for each job type
"""
def parse_parameters_file_recursive(path_to_file):
    job_data = []
    try:
        for files in os.walk(path_to_file, topdown=True, onerror=None, followlinks=False):
            for file in files[2]:
                if file == "parameters.json":
                    parameters_file_path = os.path.join(files[0], file)
                    individual_job_data = read_file_contents(parameters_file_path)
                    individual_job_data = json.loads(individual_job_data)
                    job_data.append(individual_job_data)
    except IOError as err:
        print("IO error: {0}".format(err))
    except Exception as e:
        print ("failed to open file: %s" % (str(e)))
        raise
    else:
        print "Parameters files parsed successfully"
    finally:
        job_data_sorted = sorted(job_data, key=itemgetter('job_type_name'))
        return job_data_sorted


"""
    Parse a directory and list all subdirectories in the directory
"""
def parse_subfolders_for_folder(path_to_file):
    try:
        subfolders = [f for f in listdir(path_to_file) if isfile(join(path_to_file, f))]
    except IOError:
        print "Unable to parse file name"
        raise
    else:
        print ""
        # print "File names parsed successfully"
    finally:
        return subfolders


"""
    Parse a given directory path and find a string in subfolders. This is used to find
    the job result folder for a particular job.
"""
def parse_subfolders_find_folder_name(path, folder_name_substring):
    try:
        file = int(folder_name_substring)%10
        subfolders = [f for f in listdir(path + str(file)) if isdir(join(path + str(file), f))]
        for subfolder in subfolders:
            if str(folder_name_substring) in subfolder:
                return subfolder
            else:
                continue
    except IOError as err:
        print("IO error: {0}".format(err))
    except Exception as e:
        print ("failed to open file: %s" % (str(e)))
        raise
    else:
        print "Parameters files parsed successfully"
    finally:
        return subfolder

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


