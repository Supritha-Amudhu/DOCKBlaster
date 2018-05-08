from flask import Flask
from .settings import ProdConfig
from .extensions import db, login_manager, migrate
import user, public, dock, job_results


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    from dockblaster.errors import errors_blueprint
    app.register_blueprint(errors_blueprint)

    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(dock.views.blueprint)
    app.register_blueprint(job_results.views.blueprint)
    return None

