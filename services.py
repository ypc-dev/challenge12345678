import datetime as dt
import sqlalchemy.orm as orm

import models as models, schemas as schemas, database as database


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_sensor_by_sensor_id(db: orm.Session, sensor_id: int):
  return db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()


def get_all_sensors(db: orm.Session, skip: int = 0, limit: int = 100):
  return db.query(models.Sensor).offset(skip).limit(limit).all()


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


def get_all_weatherdata(db: orm.Session, skip: int = 0, limit: int = 100):
  return db.query(models.WeatherData).offset(skip).limit(limit).all()


def get_weatherdata_by_sensor(db: orm.Session, sensor_id: int, skip: int = 0, limit: int = 100):
  return db.query(models.WeatherData).filter(models.WeatherData.sensor_id == sensor_id).offset(skip).limit(limit).all()


def get_weatherdata_in_range(db: orm.Session):
  current_time = dt.datetime.utcnow()
  ten_days_ago = current_time - dt.timedelta(days=10)
  weatherdata_in_range = db.query(models.WeatherData).filter(models.WeatherData.timestamp > ten_days_ago).all()
  return weatherdata_in_range


def create_weatherdata(db: orm.Session, weatherdata: schemas.WeatherDataCreate, sensor_id: int):
  weatherdata = models.WeatherData(**weatherdata.dict(), sensor_id=sensor_id)
  db.add(weatherdata)
  db.commit()
  db.refresh(weatherdata)
  return weatherdata


# Update services
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