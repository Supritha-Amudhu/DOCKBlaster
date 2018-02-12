from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from DOCKBlaster import app
from models import db, User, Job_Status, Docking_Job


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()