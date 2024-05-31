import multiprocessing
from .core.main import main as core_main, teardown as core_teardown
from .server.main import main as server_main, teardown as server_teardown
import logging
import signal
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def signal_handler(sig, frame):
  logging.info(f'{sig} received, tearing down')
  core_teardown()
  server_teardown()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
  to_core_queue = multiprocessing.Queue()
  to_server_queue = multiprocessing.Queue()

  core_process = multiprocessing.Process(target=core_main, args=(to_core_queue, to_server_queue))
  server_process = multiprocessing.Process(target=server_main, args=(to_core_queue, to_server_queue))

  core_process.start()
  server_process.start()

  core_process.join()
  server_process.join()

if __name__ == '__main__':
  main()