import multiprocessing
from .core.main import main as core_main
from .server.main import main as server_main
import logging
import signal
import sys
import time
import os

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

to_core_queue = multiprocessing.Queue()
to_server_queue = multiprocessing.Queue()
event = multiprocessing.Event()

core_process = multiprocessing.Process(target=core_main, args=(to_core_queue, to_server_queue, event))
server_process = multiprocessing.Process(target=server_main, args=(to_core_queue, to_server_queue, event))

def exit():
  if core_process.is_alive():
    os.kill(core_process.pid, signal.SIGINT)
  if server_process.is_alive():
    os.kill(server_process.pid, signal.SIGINT)
  core_process.join()
  server_process.join()
  sys.exit(0)

def signal_handler(sig, frame):
  logging.info(f'{sig} received, tearing down')
  exit()

signal.signal(signal.SIGINT, signal_handler)

def main():
  core_process.start()
  server_process.start()

  while True:
    if event.is_set() or not core_process.is_alive() or not server_process.is_alive():
      logging.error('Event is set or one or more subprocesses ended unexpectedly! Terminating...')
      exit()
    time.sleep(.5)


if __name__ == '__main__':
  main()