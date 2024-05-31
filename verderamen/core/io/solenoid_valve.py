from ...config import get_config_key
import RPi.GPIO as GPIO

class SolenoidValve:
  def __init__(self):
      self.valve_transistor_base_out_pin = get_config_key('VALVE_TRANSISTOR_BASE_OUT_PIN', int)
      self.keep_valve_open = get_config_key('KEEP_VALVE_OPEN', str, False) == 'True'

  def setup(self):
     GPIO.setup(self.valve_transistor_base_out_pin, GPIO.OUT)
  
  def teardown(self):
      GPIO.cleanup(self.valve_transistor_base_out_pin)

  def loop(self):
     # test
     if(self.keep_valve_open):
       GPIO.output(self.valve_transistor_base_out_pin, GPIO.HIGH)
     else:
      GPIO.output(self.valve_transistor_base_out_pin, GPIO.LOW)     
     is_open=GPIO.input(self.valve_transistor_base_out_pin)
     stats = {
        "is_open": is_open
     }
     return stats
  
  def open(self):
     GPIO.output(self.valve_transistor_base_out_pin, GPIO.HIGH)
  
  def close(self):
     GPIO.output(self.valve_transistor_base_out_pin, GPIO.LOW)