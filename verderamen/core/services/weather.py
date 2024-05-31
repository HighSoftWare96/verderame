from ..config import get_config_key 
from ..utils.numbers import rerange, weighted_mean
import requests
from urllib.parse import urljoin
import logging
from datetime import datetime

DEFAULT_WHEATER_API_BASE_URL="https://api.weatherapi.com/"
DEFAULT_WHEATER_API_FORECAST_PATH="/v1/forecast.json"

class Weather:
  def __init__(self):
    self.parse_coords()
    self.enabled=get_config_key('WEATHER_ENABLED', bool, True)
    self.api_base_url=get_config_key('WEATHER_API_BASE_URL', str, DEFAULT_WHEATER_API_BASE_URL)
    self.api_forecast_path=get_config_key('WEATHER_API_FORECAST_PATH', str, DEFAULT_WHEATER_API_FORECAST_PATH)
    self.api_key=get_config_key('WEATHER_API_API_KEY', str)
    self.high_temperature=get_config_key('WEATHER_WATER_HIGH_TEMPERATURE', int, 40)
    self.low_temperature=get_config_key('WEATHER_WATER_LOW_TEMPERATURE', int, 0)
    self.temperature_score_weight=get_config_key('WEATHER_WATER_TEMPERATURE_SCORE_WEIGHT', int, 0.8)
    self.humidity_score_weight=get_config_key('WEATHER_WATER_HUMIDITY_SCORE_WEIGHT', int, 0.3)
    self.low_rain_score_weight=get_config_key('WEATHER_WATER_LOW_RAIN_SCORE_WEIGHT', int, 1)
    self.check_weather_at_datetime=datetime.strptime(get_config_key('WEATHER_CHECK_AT_TIME', str, '12:01 AM'), '%I:%M %p')
    self.check_weather_at_range_minutes=get_config_key('WEATHER_CHECK_AT_TIME_RANGE_MINUTES', int, 5)
    self.cached_timestamp=None
    self.cached_stats=None
    self.should_retry=False
  
  def setup(self):
    self.fetch()

  
  def teardown(self):
    self.cached_stats = None
    self.cached_timestamp = None
    self.should_retry = None

  def loop(self):
    if not self.should_check_weather():
      return self.cached_stats
    
    try:
      self.should_retry = False
      self.cached_stats = None
      self.fetch()
      return self.cached_stats
    except:
      logging.exception('weather: unable to fetch for error')
      self.should_retry = True
      self.cached_stats = None
      return
  
  def should_check_weather(self):
    self.check_cache_expired()

    if self.should_retry:
      # there has been an error
      return True
  
    now = datetime.now()
    # align to current day
    self.check_weather_at_datetime.replace(day=now.day, month=now.month, year=now.year)
    time_difference_delta = now - self.check_weather_at_datetime
    time_difference_minutes = time_difference_delta.total_seconds() / 60
    operative=(time_difference_minutes >= (-1 * self.check_weather_at_range_minutes)) and (time_difference_minutes <= self.check_weather_at_range_minutes)
    return operative and self.cached_stats is None
  
  def check_cache_expired(self):
    last_checked_seconds = (23 * 60 * 60) + (30 * 60); 
    if self.cached_timestamp is not None:
      last_checked_seconds = (self.cached_timestamp - datetime.now()).total_seconds()
    if last_checked_seconds > (23 * 60 * 60) + (30 * 60):
      # passed more than 23 hours + 30 minutes, invalidate cache
      self.cached_stats = None
    
  def parse_coords(self):
    raw_coords=get_config_key('WEATHER_COORDINATES', str)
    splitted_coords=raw_coords.split(',')
    coords=list()

    for i in range(len(splitted_coords)):
      coord = float(splitted_coords[i])
      if not bool(coord):
        raise Exception('Invalid WEATHER_COORDINATES: format lat,lng')
      coords.append(coord)

    self.query_lat=coords[0]
    self.query_lng= coords[1]

  def schedule_next_run(self):
    pass

  def fetch(self):
    if not self.enabled:
      return None
    
    forecast_full_url=urljoin(self.api_base_url, self.api_forecast_path)
    params={
      "key": self.api_key,
      "q": f'{self.query_lat},{self.query_lng}',
      "days": 1,
      "aqi": 'no',
      "alerts": 'no'
    }
    headers={
      "Content-Type": "application/json"
    }

    json=None
    try:
      res=requests.get(forecast_full_url, params=params, headers=headers)
      res.raise_for_status()
      json=res.json()
      logging.info('weather: fetched forecast JSON: %s', json)
    except:
      logging.exception('weather: unable to fetch forecast data!')

    result=None
    try:
      result=self.parse_forecast(json)
    except:
      logging.exception('weather: unable to parse forecast data!')
    
    # save cached stats timestamp
    self.cached_stats=result
    self.cached_timestamp = datetime.now()


  def parse_forecast(self, json):
    forecastdays = json["forecast"]["forecastday"]
    current_day_forecast = None
    current_day_date = None

    now=datetime.now().date()
    forecast_date_epoch=forecastdays[0]["date_epoch"]
    forecast_date=datetime.fromtimestamp(forecast_date_epoch).date()
    is_today= bool(now == forecast_date)

    if not is_today:
      raise Exception('Unable to get current day forecast!')
    else:
      current_day_forecast=forecastdays[0]
      current_day_date=forecast_date

    # get current day sunset
    current_day_sunset_time=datetime.strptime(current_day_forecast["astro"]["sunset"], '%I:%M %p').time()
    current_day_sunset_datetime=datetime.combine(current_day_date, current_day_sunset_time)
    logging.info('weather: today the sun will sunset at %s', current_day_sunset_datetime)

    next_24_temp_mean = current_day_forecast["day"]["avgtemp_c"]
    next_24_temp_max = current_day_forecast["day"]["maxtemp_c"]
    next_24_temp_min = current_day_forecast["day"]["mintemp_c"]
    next_24_precip_mm = current_day_forecast["day"]["totalprecip_mm"]
    next_24_humidity_mean = current_day_forecast["day"]["avghumidity"]
    
    stats = {
      "next_24_temp_max": next_24_temp_mean,
      "next_24_temp_mean": next_24_temp_max,
      "next_24_temp_min": next_24_temp_min,
      "next_24_precip_mm": next_24_precip_mm,
      "next_24_humidity_mean": next_24_humidity_mean,
      "will_rain": next_24_precip_mm > 2
    }

    logging.info(f'weather: today conditions {current_day_forecast["day"]["condition"]["text"]}')
    logging.info(f'weather: next 24 hour stats: %s', stats)

    # water score: 0: do not water, 1: water for max time
    water_score = 1

    if stats["will_rain"]:
      water_score = 0
      logging.info(f'weather: water score 0, will rain in the next 24 hours!')
      return water_score
    
    # if 0°C will water for .1 else proportionately till 40°C
    temperature_score = rerange(stats["next_24_temp_mean"], self.low_temperature, self.high_temperature, .1, 1)
    # 0% humidity = high water score | 100% = .7 water score 
    humidity_score = rerange(stats["next_24_humidity_mean"], 0, 100, 1, .7)
    # 0mm = 1 | 2mm = .3 water score
    low_rain_score = rerange(stats["next_24_precip_mm"], 0, 2, 1, .6)
    # generate the final water score by mean all scores with a weight
    water_score = weighted_mean(
      [temperature_score, humidity_score, low_rain_score],
      [self.temperature_score_weight, self.humidity_score_weight, self.low_rain_score_weight]
    )

    scores = {
      "temperature_score": temperature_score,
      "humidity_score": humidity_score,
      "low_rain_score": low_rain_score,
    }
    logging.info(f'weather: final water score {water_score}, scores: %s!', scores)
    return water_score