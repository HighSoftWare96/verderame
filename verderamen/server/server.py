from flask import Flask
from .routes.codebase import codebase_routes
from .routes.telemetries import telemetries_routes
import logging

def build_server(to_core_q, to_server_q):
    port = 5000
    app = Flask(__name__)
    codebase_routes(to_core_q, to_server_q, app)
    telemetries_routes(to_core_q, to_server_q, app)
    logging.info(f"server: verderamen server listening on port {port}")
    logging.info('%s', app.url_map)
    app.run(host='127.0.0.1', port=(port))