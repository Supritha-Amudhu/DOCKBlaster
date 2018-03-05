from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from dockblaster.app import create_app
from dockblaster.extensions import db
from dockblaster.settings import DevConfig, ProdConfig
from flask.helpers import get_debug_flag

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(CONFIG)
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()