import datetime as dt
import sqlalchemy as sql
from database import Base

class Sensor(Base):
  __tablename__ = "sensors"
  id = sql.Column(sql.Integer, primary_key=True, index=True)
  sensor_id = sql.Column(sql.Integer, unique=True, index=True)
  country = sql.Column(sql.String)
  city = sql.Column(sql.String)


class WeatherData(Base):
  __tablename__ = "weatherdata"
  id = sql.Column(sql.Integer, primary_key=True, index=True)
  sensor_id = sql.Column(sql.Integer, sql.ForeignKey("sensors.id"))
  timestamp = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
  temp = sql.Column(sql.Integer, index=True)
  humidity = sql.Column(sql.Integer, index=True)
  wind_speed = sql.Column(sql.Integer, index=True)
  