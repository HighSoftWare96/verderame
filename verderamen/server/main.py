import logging
import sys
from .server import build_server

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

server = None

def main(to_core_q, to_server_q):
  server = build_server()

def teardown():
  pass