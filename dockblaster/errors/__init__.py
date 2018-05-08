from flask import Blueprint

errors_blueprint = Blueprint('errors', __name__)

from flask import render_template

#
# # @errors_blueprint.app_errorhandler(404)
# def not_found_error(error):
#     return render_template('error_pages/page_not_found.html'), 404
#
#
# @errors_blueprint.app_errorhandler(500)
# def internal_server_error(error):
#     return render_template('error_pages/page_not_found.html'), 500


@errors_blueprint.app_errorhandler(404)
@errors_blueprint.app_errorhandler(500)
@errors_blueprint.app_errorhandler(ValueError)
@errors_blueprint.app_errorhandler(IOError)
@errors_blueprint.app_errorhandler(EnvironmentError)
@errors_blueprint.app_errorhandler(RuntimeError)
@errors_blueprint.app_errorhandler(ImportError)
@errors_blueprint.app_errorhandler(IndexError)
@errors_blueprint.app_errorhandler(EOFError)
@errors_blueprint.app_errorhandler(ArithmeticError)
@errors_blueprint.app_errorhandler(AssertionError)
@errors_blueprint.app_errorhandler(AttributeError)
@errors_blueprint.app_errorhandler(BufferError)
@errors_blueprint.app_errorhandler(FloatingPointError)
@errors_blueprint.app_errorhandler(IndentationError)
@errors_blueprint.app_errorhandler(KeyError)
@errors_blueprint.app_errorhandler(MemoryError)
@errors_blueprint.app_errorhandler(ZeroDivisionError)
@errors_blueprint.app_errorhandler(UnicodeError)
@errors_blueprint.app_errorhandler(SystemError)
def internal_server_error(error):
    return render_template('error_pages/page_not_found.html'), 500
