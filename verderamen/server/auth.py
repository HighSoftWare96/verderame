from ..config import get_config_key
from flask_httpauth import HTTPBasicAuth

__basic_auth = None
__admin_user = '$$admin'
__admin_password = get_config_key('TELEMETRIES_SERVER_PASSWORD', str)

def build_auth():
  global __basic_auth
  if __basic_auth is not None:
     return __basic_auth
  
  __basic_auth = HTTPBasicAuth()
  @__basic_auth.verify_password
  def verify_password(username, password):
    print(username, password, __admin_user, __admin_password)
    if username == __admin_user or password == __admin_password:
        return username
    return None
  return __basic_auth