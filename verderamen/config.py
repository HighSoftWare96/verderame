from os import environ

def get_config_key(key, ctor, defaultValue = None):
  if key in environ:
    return ctor(environ[key])
  if not bool(defaultValue):
    raise Exception(f'Configuration key {key} required!')
  return defaultValue
