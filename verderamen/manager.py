import RPi.GPIO as GPIO
from .io.tank_level import TankLevel
from .io.solenoid_valve import SolenoidValve
from time import sleep

class Manager:
  def __init__(self):
    self.tank = TankLevel()
    self.valve = SolenoidValve()

  def __del__(self):
    GPIO.cleanup()

  def setup(self):
    GPIO.setmode(GPIO.BCM)
    self.tank.setup()
    self.valve.setup()

  def loop(self):
    tank_stats = self.tank.loop()
    valve_stats = self.valve.loop()
    print(f'current tank level: {tank_stats["percentage"]}% (water level from top: {tank_stats["avg"]}cm)')
    print(f'is valve open? {valve_stats['is_open']}')
    sleep(5)