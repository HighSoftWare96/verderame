from .manager import Manager
import sys
import signal

manager = Manager()

def signal_handler(sig, frame):
  print(f'{sig} received, tearing down')
  manager.teardown()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
  try:
    print('Manager setup running...')
    manager.setup()
    print('Manager setup done! Starting main loop...')
    while(True):
      manager.loop()
  finally:
    manager.teardown()


if __name__ == '__main__':
  print('Starting...')
  main()