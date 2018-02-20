from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from DOCKBlaster import app

login_manager = LoginManager(app)
db = SQLAlchemy()
migrate = Migrate()
