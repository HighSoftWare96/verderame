from .manager import Manager
import sys
import logging
import signal

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
manager = Manager()

def teardown():
  if manager:
    manager.teardown()

def signal_handler(sig, frame):
  logging.info(f'core: {sig} received, tearing down')
  teardown()

signal.signal(signal.SIGINT, signal_handler)

def main(to_core_q, to_server_q, event):
  try:
    logging.info('core: manager setup running...')
    manager.setup()
    logging.info('core: manager setup done! Starting main loop...')
    while True:
      manager.loop()
  except:
    logging.exception('core: process failure for exception...')
    event.set()