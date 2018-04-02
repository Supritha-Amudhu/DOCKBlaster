import errno
import os
from os import listdir
from os.path import join, isfile, isdir
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
    except IOError as err:
        print("IO error: {0}".format(err))
    else:
        print "File read successfuly"
    finally:
        f.close()


def generate_result_file(upload_folder, receptorFile_contents, ligandFile_contents, expertFile_contents):
    try:
        with open(str(upload_folder) + "/output.txt", "wb") as fo:
            fo.write(receptorFile_contents + "\n" + ligandFile_contents + "\n" + expertFile_contents)
            return 1
    except Exception as e:
        print ("Error: %s" % (str(e)))
        raise
    finally:
        fo.close()

def parse_parameters_file(path_to_file):
    try:
        data = json.load(open(path_to_file))
    except IOError as err:
        print("IO error: {0}".format(err))
        raise
    else:
        print "Parameters file parsed successfully"
    return data


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
        return job_data


def parse_subfolders_for_folder(path_to_file):
    try:
        subfolders = [f for f in listdir(path_to_file) if isfile(join(path_to_file, f))]
    except IOError:
        print "Unable to parse file name"
        raise
    else:
        print "File names parsed successfully"
    finally:
        return subfolders


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


