from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from DOCKBlaster import app
from dockblaster.extensions import db
from dockblaster.user.models import User
from dockblaster.fileupload.models import Job_Status, Docking_Job

migrate = Migrate(app, db)
manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/dockblaster"

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()