UPLOAD_FOLDER = '/Users/supritha/Workspace/PycharmProjects/DOCKBlaster/Files'
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_file_contents(file):
    with open(file, "r") as f:
        content = f.read()
        return content


def generate_result_file(file_a_contents, file_b_contents):
    with open("/Users/supritha/Workspace/PycharmProjects/DOCKBlaster/Files/output.txt", "wb") as fo:
        fo.write(file_a_contents + "\n" + file_b_contents)
        return 1