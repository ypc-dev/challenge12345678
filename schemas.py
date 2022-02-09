from typing import List
import datetime as dt
import pydantic as pydantic


class _SensorBase(pydantic.BaseModel):
  sensor_id: int
  country: str
  city: str


class SensorCreate(_SensorBase):
  pass


class Sensor(_SensorBase):
  class Config:
    orm_mode = True


class _WeatherDataBase(pydantic.BaseModel):
  temp: int
  humidity: int
  wind_speed: int


class WeatherDataCreate(_WeatherDataBase):
  pass


class WeatherData(_WeatherDataBase):
  id: int
  sensor_id: int
  timestamp: dt.datetime

  class Config:
    orm_mode = True


class WeatherDataMetrics(pydantic.BaseModel):
  weatherdata: List[WeatherData]
  avg_temp: float
  avg_humidity: float
  avg_wind_speed: float


class WeatherDataUpdate(_WeatherDataBase):
  timestamp: dt.datetime