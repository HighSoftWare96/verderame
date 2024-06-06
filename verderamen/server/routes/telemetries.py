from os import path
from ...services.intercom import list_messages
from ..auth import build_auth
from os import getpid

current_file_name=f"/{path.basename(__file__).replace('.py', '')}"
__cached_telemetries = None

def telemetries_routes(to_core_q, to_server_q, app, prefix = current_file_name):
   auth = build_auth()

   @app.route(path.join(prefix, ''), methods=['GET'])
   @auth.login_required
   def getTelemetries():
      msgs = list_messages(to_server_q)
      if bool(len(msgs)):
         __cached_telemetries = msgs[0].payload
      __cached_telemetries['process']['server_pid'] = getpid()
      return __cached_telemetries
