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
    logging.info(f'tank: current level {tank_stats["stats"]["percentage"]}% (water level from top: {tank_stats["stats"]["avg"]}cm)')
    logging.info(f'valve: is valve open? {bool(valve_stats["stats"]["is_open"])}')
    logging.info('weather: stats %s', weather_stats)
    return {
      "tank": tank_stats,
      "valve": valve_stats,
      "weather": weather_stats
    }