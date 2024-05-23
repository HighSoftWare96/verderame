from ..config import get_config_key
import RPi.GPIO as GPIO

class SolenoidValve:
  def __init__(self):
      self.valve_transistor_base_out_pin = get_config_key('VALVE_TRANSISTOR_BASE_OUT_PIN', int)

  def setup(self):
     GPIO.setup(self.valve_transistor_base_out_pin, GPIO.OUT)

  def loop(self):
     # test
     GPIO.output(self.valve_transistor_base_out_pin, GPIO.HIGH)
     is_open=GPIO.input(self.valve_transistor_base_out_pin)
     return {
        "is_open": is_open
     }
  
  def open(self):
     GPIO.output(self.valve_transistor_base_out_pin, GPIO.HIGH)
  
  def close(self):
     GPIO.output(self.valve_transistor_base_out_pin, GPIO.LOW)