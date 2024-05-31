import time
import RPi.GPIO as GPIO
from ...config import get_config_key

class TankLevel:
    def __init__(self):
      self.tank_level_out_pin = get_config_key('TANK_LEVEL_OUT_PIN', int)
      self.tank_level_in_pin = get_config_key('TANK_LEVEL_IN_PIN', int)
      self.tank_level_min_distance_cm= get_config_key('TANK_LEVEL_MIN_DISTANCE_CM', int)
      self.tank_level_max_distance_cm= get_config_key('TANK_LEVEL_MAX_DISTANCE_CM', int)
      self.distance_interval=self.tank_level_max_distance_cm - self.tank_level_min_distance_cm
      self.sound_speed = 34340
        
    def setup(self):
      GPIO.setup(self.tank_level_in_pin, GPIO.IN)
      GPIO.setup(self.tank_level_out_pin, GPIO.OUT)
  
    def teardown(self):
      GPIO.cleanup([self.tank_level_in_pin, self.tank_level_out_pin])
    
    def loop(self):
      avg = self.measure_avg()
      percentage = self.measure_percentage()
      stats = {
        'percentage': percentage,
        'avg': avg
      }
      return {
        "stats": stats,
        "scores": {
           "final_score": int(stats["percentage"] > 5) 
        }
      }
      

    def measure_one(self):
        GPIO.output(self.tank_level_out_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.tank_level_out_pin, GPIO.LOW)

        start = time.time()

        while GPIO.input(self.tank_level_in_pin) == GPIO.LOW:
            start = time.time()

        while GPIO.input(self.tank_level_in_pin) == GPIO.HIGH:
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