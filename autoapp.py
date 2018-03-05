# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from dockblaster.app import create_app
from dockblaster.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(CONFIG)
#app.run()
app.run(host='0.0.0.0', port=5001, debug=True)
