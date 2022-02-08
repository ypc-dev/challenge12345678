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


def create_weatherdata(db: orm.Session, weatherdata: schemas.WeatherDataCreate, sensor_id: int):
  weatherdata = models.WeatherData(**weatherdata.dict(), sensor_id=sensor_id)
  db.add(weatherdata)
  db.commit()
  db.refresh(weatherdata)
  return weatherdata


