import errno
import os

ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file_contents(file):
    with open(file, "r") as f:
        content = f.read()
        return content


def generate_result_file(upload_folder, receptorFile_contents, ligandFile_contents, expertFile_contents):
    with open(str(upload_folder) + "/output.txt", "wb") as fo:
        fo.write(receptorFile_contents + "\n" + ligandFile_contents + "\n" + expertFile_contents)
        return 1

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


