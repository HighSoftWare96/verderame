from .manager import Manager
import sys
import logging
import signal

manager = Manager()

'''
def signal_handler(sig, frame):
  logging.info(f'{sig} received, tearing down')
  manager.teardown()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
'''

def main():
  try:
    logging.info('Manager setup running...')
    manager.setup()
    logging.info('Manager setup done! Starting main loop...')
    while(True):
      manager.loop()
  finally:
    manager.teardown()


if __name__ == '__main__':
  logging.info('Starting...')
  main()