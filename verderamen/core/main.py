#from .manager import Manager
import sys
import logging

def main(to_core_q, to_server_q, event):
  logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
  try:
    logging.info('core: manager setup running...')
    # manager.setup()
    logging.info('core: manager setup done! Starting main loop...')
    while not event.is_set():
      print('', end='')
      # manager.loop()
  except KeyboardInterrupt:
    logging.info('core: KeyboardInterrupt received!')
  finally:
    logging.info('core: tearing down...')