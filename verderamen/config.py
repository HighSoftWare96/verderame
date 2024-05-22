from os import environ

def get_config_key(key, default = None):
  if key in environ:
    return environ[key]
  if not default:
    raise Exception(f'Configuration key {key} required!')
  return default
