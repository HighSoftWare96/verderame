from os import path
from ...services.intercom import list_messages
from ..auth import basic_auth

current_file_name=f"/{path.basename(__file__).replace('.py', '')}"
__cached_telemetries = None

def telemetries_routes(to_core_q, to_server_q, app, prefix = current_file_name):
    @app.route(path.join(prefix, ''), methods=['GET'])
    @basic_auth.login_required
    def getTelemetries():
      msgs = list_messages(to_server_q)
      if bool(len(msgs)):
         __cached_telemetries = msgs[0].payload
      return __cached_telemetries
