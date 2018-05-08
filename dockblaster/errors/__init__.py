from flask import Blueprint

errors_blueprint = Blueprint('errors', __name__)

from flask import render_template
from autoapp import app


@app.errorhandler(404)
@errors_blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('error_pages/page_not_found.html'), 404


@app.errorhandler(500)
@errors_blueprint.app_errorhandler(500)
def not_found_error(error):
    return render_template('error_pages/page_not_found.html'), 500


