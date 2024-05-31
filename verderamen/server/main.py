import logging
import sys
from .server import build_server

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def main(to_core_q, to_server_q, event):
  try:
    build_server()
  except:
    logging.exception('server: process failure for exception...')
    event.set()