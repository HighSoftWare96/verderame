from datetime import datetime
from multiprocessing import Queue
from os import path
import json
import pickle

QUEUE_MAX_SIZE = 10
QUEUES = {
  "verderamen-to-server": "../.to-server.queue.bin",
  "server-to-verderamen": "../.to-verderamen.queue.bin"
}

INTERCOM_MESSAGE_TYPES = {
  "telemetries": 'TELEMETRIES',
  "water_override_command": "WATER_OVERRIDE_COMMAND"
}

class IntercomMessage:
  def __init__(self, type, payload = {}, timestamp = datetime.now()):
    if type not in INTERCOM_MESSAGE_TYPES.values():
      raise('Expected INTERCOM_MESSAGE_TYPES type!')
    self.type = type
    self.payload = payload
    self.timestamp = timestamp

  def to_json(self) -> str:
    return json.dumps({
      "type": self.type,
      "payload": self.payload,
      "timestamp": self.timestamp.isoformat()
    })


def enqueue_message(queueName, type, payload, emptyQueueFirst = False) -> IntercomMessage:
  message = IntercomMessage(type, payload)
  encoded = message.to_json()
  def send_message(queue):
    while emptyQueueFirst and not queue.empty():
      queue.get(timeout=50)
    queue.put(encoded)
  sync_queue_file(queueName, send_message)
  

def list_messages(queueName):
  def unravel_queue(queue):
    emptied = False
    messages = []
    while not emptied:
      try:
        message = queue.get(timeout=200)
        decoded = json.load(message)
        intercom_message = IntercomMessage(decoded["type"], decoded["payload"], decoded["timestamp"])
        messages.append(intercom_message)
      except queue.Empty:
        emptied = True
    return messages
  return sync_queue_file(queueName, unravel_queue)


def sync_queue_file(queue_name, handler):
  if queue_name not in QUEUES:
    raise('Expected valid queue!')

  ensure_queue(queue_name)
  queue_file_path = QUEUES[queue_name]
  with open(queue_file_path, 'wb') as queue_file:
    # reload current queue
    queue = pickle.load(queue_file)
    # do things with queue
    result = handler(queue)
    # dump queue
    pickle.dump(queue, queue_file)
    return result
  
def ensure_queue(queue_name):
  if queue_name not in QUEUES:
    raise('Expected valid queue!')
  
  queue_file_path = QUEUES[queue_name]
  exists = path.exists(queue_file_path)
  
  if exists:
    return
  
  with open(queue_file_path, 'wb') as queue_file:
    new_queue = Queue(QUEUE_MAX_SIZE)
    pickle.dump(new_queue, queue_file)