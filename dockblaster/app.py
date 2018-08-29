import flask_admin
from flask import Flask

from dockblaster.admin.model_views import AdminModelView
from dockblaster.dock_jobs.models import Job_Type, Docking_Job, Job_Status
from dockblaster.user.models import User
from .settings import ProdConfig
from .extensions import db, login_manager, migrate
import user, public, dock_jobs, docking_results
from flask_admin.contrib.sqla import ModelView

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    admin = flask_admin.Admin(app, name='DOCKBlaster', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, "Users", endpoint="users_"))
    admin.add_view(ModelView(Docking_Job, db.session, "Docking Jobs"))
    admin.add_view(ModelView(Job_Type, db.session, "Job Types"))
    admin.add_view(ModelView(Job_Status, db.session, "Job Statuses"))

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
    app.register_blueprint(user.views.user_blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(dock_jobs.views.blueprint)
    app.register_blueprint(docking_results.views.blueprint)
    return None

