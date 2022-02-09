from typing import List
import datetime as dt
from pydantic import BaseModel


class _SensorBase(BaseModel):
  sensor_id: int
  country: str
  city: str


class SensorCreate(_SensorBase):
  pass


class Sensor(_SensorBase):
  class Config:
    orm_mode = True


class _WeatherDataBase(BaseModel):
  temp: float
  humidity: float
  wind_speed: float


class WeatherDataCreate(_WeatherDataBase):
  pass


class WeatherData(_WeatherDataBase):
  id: int
  sensor_id: int
  timestamp: dt.datetime

  class Config:
    orm_mode = True


class WeatherDataMetrics(BaseModel):
  weatherdata: List[WeatherData]
  avg_temp: float
  avg_humidity: float
  avg_wind_speed: float


class WeatherDataUpdate(_WeatherDataBase):
  timestamp: dt.datetime