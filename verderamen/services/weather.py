from ..config import get_config_key 
from ..utils.numbers import rerange, weighted_mean
import requests
from urllib.parse import urljoin
import logging
from datetime import datetime

DEFAULT_WHEATER_API_BASE_URL="https://api.weatherapi.com/v1/"
DEFAULT_WHEATER_API_FORECAST_PATH="/forecast.json"

class Weather:
  def __init__(self):
    self.parse_coords()
    self.api_base_url=get_config_key('WEATHER_API_BASE_URL', str, DEFAULT_WHEATER_API_BASE_URL)
    self.api_forecast_path=get_config_key('WEATHER_API_FORECAST_PATH', str, DEFAULT_WHEATER_API_FORECAST_PATH)
    self.api_key=get_config_key('WEATHER_API_API_KEY', str)
    self.high_temperature=get_config_key('WEATHER_WATER_HIGH_TEMPERATURE', int, 40)
    self.low_temperature=get_config_key('WEATHER_WATER_LOW_TEMPERATURE', int, 0)
    self.temperature_score_weight=get_config_key('WEATHER_WATER_TEMPERATURE_SCORE', int, 0.8)
    self.humidity_score_weight=get_config_key('WEATHER_WATER_HUMIDITY_SCORE_WEIGHT', int, 0.3)
    self.low_rain_score_weight=get_config_key('WEATHER_WATER_LOW_RAIN_SCORE_WEIGHT', int, 1)
    self.check_weather_at_time=datetime.strptime(get_config_key('WEATHER_CHECK_AT_TIME', str, '12:00 AM'), '%I:%M %p').time()
    self.cached_stats=None
    self.should_retry=False
  
  def setup(self):
    pass

  
  def teardown(self):
    pass

  def loop(self):
    if not self.should_check_weather():
      return self.cached_stats
    
    try:
      self.should_retry = False
      self.cached_stats = None
      self.cached_stats = self.fetch()
      return self.cached_stats
    except:
      logging.exception('Weather: unable to fetch for error')
      self.should_retry = True
      self.cached_stats = None
      return
  
  def should_check_weather(self):
    if self.should_retry:
      return True
    operative=(datetime.now().strftime('%I:%M %p') == self.check_weather_at_time.strftime('%I:%M %p'))
    return operative and self.cached_stats is None
    
    
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

  def fetch(self):
    forecast_full_url=urljoin(self.api_base_url, self.api_forecast_path)
    params={
      "key": self.api_key,
      "q": f'{self.query_lat},{self.query_lng}',
      "days": 2,
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
      logging.info('Forecast JSON: %s', json)
    except:
      logging.exception('Weather: unable to fetch forecast data!')

    try:
      result=self.parse_forecast(json)
    except:
      logging.exception('Weather: unable to parse forecast data!')


  def parse_forecast(self, json):
    forecastdays = json["forecast"]["forecastday"]
    current_day_forecast = None
    current_day_date = None
    next_day_forecast = None
    next_day_date = None

    for forecastday in forecastdays:
      forecast_date_epoch=forecastday["date_epoch"]
      forecast_date=datetime.fromtimestamp(forecast_date_epoch).date()
      now=datetime.now().date()
      is_today= bool(now == forecast_date)

      if is_today:
        current_day_forecast=forecastday
        current_day_date=forecast_date
      else:
        next_day_forecast=forecastday
        next_day_date=forecast_date

    if current_day_forecast is None or next_day_forecast is None:
      raise Exception('Unable to find current day forecast or next day forecast')

    # get current day sunset
    current_day_sunset_time=datetime.strptime(current_day_forecast["astro"]["sunset"], '%I:%M %p').time()
    current_day_sunset_datetime=datetime.combine(current_day_date, current_day_sunset_time)
    logging.info('Weather: today the sun will sunset at %s', current_day_sunset_datetime)

    next_24_temp_mean = (current_day_forecast["day"]["avgtemp_c"] + next_day_forecast["day"]["avgtemp_c"]) / 2
    next_24_temp_max = max(current_day_forecast["day"]["maxtemp_c"], next_day_forecast["day"]["maxtemp_c"])
    next_24_temp_min = min(current_day_forecast["day"]["mintemp_c"], next_day_forecast["day"]["mintemp_c"])
    next_24_precip_mm = (current_day_forecast["day"]["totalprecip_mm"] + next_day_forecast["day"]["totalprecip_mm"])
    next_24_humidity_mean = (current_day_forecast["day"]["avghumidity"] + next_day_forecast["day"]["avghumidity"]) / 2
    
    stats = {
      "next_24_temp_max": next_24_temp_mean,
      "next_24_temp_mean": next_24_temp_max,
      "next_24_temp_min": next_24_temp_min,
      "next_24_precip_mm": next_24_precip_mm,
      "next_24_humidity_mean": next_24_humidity_mean,
      "will_rain": next_24_precip_mm > 2
    }

    logging.info(f'Weather: today condition {current_day_forecast["day"]["condition"]["text"]}')
    logging.info(f'Weather: tomorrow condition {next_day_forecast["day"]["condition"]["text"]}')
    logging.info(f'Weather: next 24 hour stats: %s', stats)

    # water score: 0: do not water, 1: water for max time
    water_score = 1

    if stats["will_rain"]:
      water_score = 0
      logging.info(f'Weather: water score 0, will rain in the next 24 hours!')
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
    logging.info(f'Weather: final water score {water_score}, scores: %s!', scores)
    return water_score