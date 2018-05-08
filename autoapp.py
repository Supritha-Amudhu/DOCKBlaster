# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from dockblaster.app import create_app
from dockblaster.settings import DevConfig, ProdConfig


CONFIG = DevConfig if get_debug_flag() else ProdConfig

#
# def app(environ, start_response):
#     """Simplest possible application object"""
#     data = 'Hello, World!\n'
#     status = '200 OK'
#     response_headers = [
#         ('Content-type','text/plain'),
#         ('Content-Length', str(len(data)))
#     ]
#     start_response(status, response_headers)
#     return iter([data])


app = create_app(CONFIG)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


