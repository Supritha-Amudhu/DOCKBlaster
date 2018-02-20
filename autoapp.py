# -*- coding: utf-8 -*-
"""Create an application instance."""

from dockblaster.app import create_app
from dockblaster.settings import DevConfig

#CONFIG = DevConfig if get_debug_flag() else ProdConfig
CONFIG = DevConfig

app = create_app(CONFIG)

app.run()