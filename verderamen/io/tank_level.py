import time
import RPi.GPIO as GPIO
from ..config import get_config_key
 
GPIO.setmode(GPIO.BCM)

class TankLevel:
    def __init__(self):
      self.tank_level_out_pin = get_config_key('TANK_LEVEL_OUT_PIN')
      self.tank_level_in_pin = get_config_key('TANK_LEVEL_IN_PIN')
      self.TANK_LEVEL_MIN_DISTANCE_CM= get_config_key('TANK_LEVEL_MIN_DISTANCE_CM')
      self.TANK_LEVEL_MAX_DISTANCE_CM= get_config_key('TANK_LEVEL_MAX_DISTANCE_CM')
      self.distance_interval=self.TANK_LEVEL_MAX_DISTANCE_CM - self.TANK_LEVEL_MIN_DISTANCE_CM
      self.sound_speed = 34340
        
    def __del__(self):
        GPIO.cleanup()
        
    def setup(self):
      pass
    
    def loop(self):
      avg = self.measure_avg()
      percentage = self.measure_percentage()
      stats = {
        'percentage': percentage,
        'avg': avg
      }
      return stats
      

    def measure_one(self):
        GPIO.output(self.tank_level_out_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.tank_level_out_pin, False)

        start = time.time()

        while GPIO.input(self.tank_level_in_pin) == 0:
            start = time.time()

        while GPIO.input(self.tank_level_in_pin) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * self.sound_speed) / 2

        return distance
      
    def measure_avg(self, samples_count = 5):
        result = 0
        for _ in range(0, samples_count):
          result += self.measure_one()
        return float(result / samples_count)

    def measure_percentage(self, samples_count = 1):
        average = self.measure_avg(samples_count)
        return float((average / self.distance_interval) * 100)