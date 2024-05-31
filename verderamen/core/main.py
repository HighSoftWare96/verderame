from .manager import Manager
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
manager = Manager()

def main(to_core_q, to_server_q):
  try:
    logging.info('Manager setup running...')
    manager.setup()
    logging.info('Manager setup done! Starting main loop...')
    while(True):
      manager.loop()
  finally:
    manager.teardown()

def teardown():
  if manager:
    manager.teardown()