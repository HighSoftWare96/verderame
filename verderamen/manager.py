import RPi.GPIO as GPIO
from .io.tank_level import TankLevel

class Manager:
  def __init__(self):
    self.tank = TankLevel()

  def __del__(self):
    GPIO.cleanup()

  def setup(self):
    GPIO.setmode(GPIO.BCM)
    self.tank.setup()

  def loop(self):
    tank_stats = self.tank.loop()
    print(f'current tank level: {tank_stats["percentage"]}% (water level from top: {tank_stats["avg"]}cm)')