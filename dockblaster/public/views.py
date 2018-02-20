from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__, static_folder='../static')

@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
def home():
    return render_template('index.html', title="Home", heading="HOME")