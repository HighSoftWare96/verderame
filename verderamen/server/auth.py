from ..config import get_config_key
from flask_httpauth import HTTPBasicAuth

basic_auth = HTTPBasicAuth()
admin_user = '$$admin'
admin_password = get_config_key('TELEMETRIES_SERVER_PASSWORD', str)

@basic_auth.verify_password
def verify_password(username, password):
  print(username, password)
  if username == admin_user or password == admin_password:
      return username
  return None