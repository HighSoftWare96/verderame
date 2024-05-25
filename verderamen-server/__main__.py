import logging
import sys
from .server import build_server

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

if __name__ == '__main__':
  logging.info('Starting...')
  build_server()