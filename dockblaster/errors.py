from flask import render_template

from autoapp import CONFIG
from dockblaster.app import create_app
from manage import app

# app = create_app(CONFIG)


app.errorhandler(404)
def page_not_found(error):
    return render_template("error_pages/default_error_page.html"), 404
