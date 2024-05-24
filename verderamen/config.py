from os import environ

def get_config_key(key, ctor, defaultValue = None):
  if key in environ:
    if ctor == bool:
      return environ[key].lower() == 'true'
    return ctor(environ[key])
  elif defaultValue is None:
    raise Exception(f'Configuration key {key} required!')
  return defaultValue
