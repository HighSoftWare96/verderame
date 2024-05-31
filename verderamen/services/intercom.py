from datetime import datetime
from queue import Empty
import json

QUEUE_MAX_SIZE = 10
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


def enqueue_message(queue, type, payload, emptyQueueFirst = False) -> IntercomMessage:
  message = IntercomMessage(type, payload)
  encoded = message.to_json()
  while emptyQueueFirst and not queue.empty():
    queue.get(timeout=50)
  queue.put(encoded)
  return message
  

def list_messages(queue):
  emptied = False
  messages = []
  while not emptied:
    try:
      message = queue.get(timeout=.3)
      decoded = json.loads(message)
      print(decoded)
      intercom_message = IntercomMessage(decoded["type"], decoded["payload"], decoded["timestamp"])
      messages.append(intercom_message)
    except Empty:
      print('emptied')
      emptied = True
  print(messages)
  return messages
