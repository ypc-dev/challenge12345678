import datetime as dt
import sqlalchemy.orm as orm
import sqlalchemy as sql
import models as models, schemas as schemas, database as database


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

##### CRUD for 'sensors' Table #####

def create_sensor(db: orm.Session, sensor: schemas.SensorCreate):
  db_sensor = models.Sensor(
    sensor_id=sensor.sensor_id,
    country=sensor.country,
    city=sensor.city
  )
  db.add(db_sensor)
  db.commit()
  db.refresh(db_sensor)
  return db_sensor


def get_sensor_by_sensor_id(db: orm.Session, sensor_id: int):
  return db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()


def get_all_sensors(db: orm.Session, skip: int = 0, limit: int = 100):
  return db.query(models.Sensor).offset(skip).limit(limit).all()


##### CRUD for 'weatherdata' Table #####

def create_weatherdata(db: orm.Session, weatherdata: schemas.WeatherDataCreate, sensor_id: int):
  weatherdata = models.WeatherData(**weatherdata.dict(), sensor_id=sensor_id)
  db.add(weatherdata)
  db.commit()
  db.refresh(weatherdata)
  return weatherdata


def get_all_weatherdata(db: orm.Session, day_range: int = 1, skip: int = 0, limit: int = 100):
  time_delta = calculate_time_delta(day_range)
  weatherdata = db.query(models.WeatherData).filter(models.WeatherData.timestamp > time_delta).offset(skip).limit(limit).all()
  avg_temp = db.query(models.WeatherData).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.temp)).scalar()
  avg_humidity = db.query(models.WeatherData).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.humidity)).scalar()
  avg_wind_speed = db.query(models.WeatherData).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.wind_speed)).scalar()

  result = schemas.WeatherDataMetrics(
    weatherdata = weatherdata, 
    avg_temp = round(avg_temp, 2), 
    avg_humidity = round(avg_humidity, 2), 
    avg_wind_speed = round(avg_wind_speed, 2)
  )
  return result


def get_weatherdata_by_sensor(db: orm.Session, sensor_id: int, day_range: int, skip: int = 0, limit: int = 100):
  time_delta = calculate_time_delta(day_range)
  weatherdata = db.query(models.WeatherData).filter(models.WeatherData.sensor_id == sensor_id).filter(models.WeatherData.timestamp > time_delta).offset(skip).limit(limit).all()
  avg_temp = db.query(models.WeatherData).filter(models.WeatherData.sensor_id == sensor_id).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.temp)).scalar()
  avg_humidity = db.query(models.WeatherData).filter(models.WeatherData.sensor_id == sensor_id).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.humidity)).scalar()
  avg_wind_speed = db.query(models.WeatherData).filter(models.WeatherData.sensor_id == sensor_id).filter(models.WeatherData.timestamp > time_delta).with_entities(sql.func.avg(models.WeatherData.wind_speed)).scalar()

  result = schemas.WeatherDataMetrics(
    weatherdata = weatherdata, 
    avg_temp = round(avg_temp, 2), 
    avg_humidity = round(avg_humidity, 2), 
    avg_wind_speed = round(avg_wind_speed, 2)
  )
  return result


def get_weatherdata(db: orm.Session, id: int):
  return db.query(models.WeatherData).filter(models.WeatherData.id == id).first()


def update_weatherdata(db: orm.Session, id: int, weatherdata: schemas.WeatherDataUpdate):
  db_weatherdata = get_weatherdata(db=db, id=id)
  db_weatherdata.timestamp = weatherdata.timestamp
  db_weatherdata.temp = weatherdata.temp
  db_weatherdata.humidity = weatherdata.humidity
  db_weatherdata.wind_speed = weatherdata.wind_speed
  db.commit()
  db.refresh(db_weatherdata)
  return db_weatherdata


##### Helper Functions #####

def calculate_time_delta(day_range: int):
  current_time = dt.datetime.utcnow()
  time_delta = current_time - dt.timedelta(days=day_range)
  return time_delta