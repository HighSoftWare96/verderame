import RPi.GPIO as GPIO
import logging
from .services.weather import Weather
from .io.tank_level import TankLevel
from .io.solenoid_valve import SolenoidValve
from time import sleep

class Manager:
  def __init__(self):
    self.tank = TankLevel()
    self.valve = SolenoidValve()
    self.weather = Weather()

  def setup(self):
    GPIO.setmode(GPIO.BCM)
    self.tank.setup()
    self.valve.setup()
    self.weather.setup()
  
  def teardown(self):
    self.tank.teardown()
    self.valve.teardown()
    self.weather.teardown()
    GPIO.cleanup()

  def loop(self):
    tank_stats = self.tank.loop()
    valve_stats = self.valve.loop()
    weather_stats = self.weather.loop()
    logging.info(f'current tank level: {tank_stats["percentage"]}% (water level from top: {tank_stats["avg"]}cm)')
    logging.info(f'is valve open? {valve_stats["is_open"]}')
    sleep(5)