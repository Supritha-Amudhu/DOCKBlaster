from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__, static_folder='../static')

@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="DOCK Blaster 18", heading="DOCK Blaster 18")