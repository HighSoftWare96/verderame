from flask import Flask
from .routes.codebase import codebase_routes
import logging

def build_server():
    port = 5000
    app = Flask(__name__)
    codebase_routes(app)
    app.run(host='127.0.0.1', port=(port))
    logging.info(f"server: verderamen server listening on port {port}")
    logging.info('%s', app.url_map)
