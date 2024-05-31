import logging
import sys
from .server import build_server

def main(to_core_q, to_server_q, event):
  logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
  build_server()
