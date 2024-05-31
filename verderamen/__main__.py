import multiprocessing
from .core.main import main as core_main
from .server.main import main as server_main
import logging
import signal
import sys
from os import getpid
import time

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def main():
  to_core_queue = multiprocessing.Queue()
  to_server_queue = multiprocessing.Queue()
  event = multiprocessing.Event()

  core_process = multiprocessing.Process(target=core_main, args=(to_core_queue, to_server_queue, event))
  server_process = multiprocessing.Process(target=server_main, args=(to_core_queue, to_server_queue, event))

  core_process.start()
  server_process.start()
  logging.info(f'parent: current PID {getpid()} started processes with PID core:{core_process.pid}, server:{server_process.pid}')

  def exit():
    logging.info('exiting...')
    event.set()
    core_process.join()
    server_process.terminate()
    server_process.join()
  
  def signal_handler(sig, frame):
    logging.info(f'parent: {sig} received, tearing down')
    exit()

  signal.signal(signal.SIGINT, signal_handler)
    
  try:
    while core_process.is_alive() and server_process.is_alive():
      time.sleep(.5)
  finally:
    exit()


if __name__ == '__main__':
  main()