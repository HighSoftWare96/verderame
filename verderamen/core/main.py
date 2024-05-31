from .manager import Manager
import sys
from time import sleep
from ..services.intercom import INTERCOM_MESSAGE_TYPES, enqueue_message
import logging
from datetime import datetime
from os import getpid, getppid
from psutil import cpu_percent, virtual_memory, sensors_temperatures

start_time = datetime.now()

def send_telemetries(to_server_q, telemetries):
  full_report = {
    "os": {
      "cpu_used": cpu_percent(1, percpu=False),
      "mem_used": virtual_memory().percent,
      "cpu_temp_celsius": sensors_temperatures()['cpu_thermal'][0].current
    },
    "process": {
      "parent_pid": getppid(),
      "core_pid": getpid(),
      "sttime": start_time.isoformat(),
      "uptime": (datetime.now() - start_time).total_seconds()
    },
    "telemetries": telemetries
  }
  enqueue_message(to_server_q, INTERCOM_MESSAGE_TYPES["telemetries"], full_report, emptyQueueFirst=True)

def main(to_core_q, to_server_q, event):
  logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
  manager = Manager() 

  try:
    logging.info('core: manager setup running...')
    manager.setup()
    logging.info('core: manager setup done! Starting main loop...')

    while not event.is_set():
      telemetries = manager.loop()
      send_telemetries(to_server_q, telemetries)
      sleep(5)

  except KeyboardInterrupt:
    logging.info('core: KeyboardInterrupt received!')
  finally:
    logging.info('core: tearing down...')
    manager.teardown()