from typing import List
import fastapi as fastapi
import sqlalchemy.orm as orm
import services as services, schemas as schemas

app = fastapi.FastAPI()

services.create_database()

@app.get("/")
def home():
  return {"message": "Yitpin's Code Challenge"}


@app.post("/sensors/", response_model=schemas.Sensor)
def create_sensor(
  sensor: schemas.SensorCreate,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  db_sensor = services.get_sensor_by_sensor_id(db=db, sensor_id=sensor.sensor_id)
  if db_sensor:
    raise fastapi.HTTPException(
      status_code=400, 
      detail="A sensor with this ID already exists!"
    )
  return services.create_sensor(db=db, sensor=sensor)


@app.get("/sensors/", response_model=List[schemas.Sensor])
def get_all_sensors(
  skip: int = 0,
  limit: int = 50,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  sensors = services.get_all_sensors(db=db, skip=skip, limit=limit)
  return sensors


@app.get("/sensors/{sensor_id}", response_model=schemas.Sensor)
def get_sensor(
  sensor_id: int,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  db_sensor = services.get_sensor_by_sensor_id(db=db, sensor_id=sensor_id)
  if db_sensor is None:
    raise fastapi.HTTPException(
      status_code=400, 
      detail="A sensor with this ID does not exists!"
    )
  return db_sensor

@app.get("/sensors/{sensor_id}/weatherdata", response_model=List[schemas.WeatherData])
def get_weatherdata_by_sensor(
  sensor_id: int,
  skip: int = 0,
  limit: int = 50,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  db_sensor = services.get_sensor_by_sensor_id(db=db, sensor_id=sensor_id)
  if db_sensor is None:
    raise fastapi.HTTPException(
      status_code=400, 
      detail="A sensor with this ID does not exists!"
    )
  return services.get_weatherdata_by_sensor(db=db, sensor_id=sensor_id, skip=skip, limit=limit)

@app.post("/sensors/{sensor_id}/weatherdata", response_model=schemas.WeatherData)
def create_weatherdata(
  sensor_id: int,
  weatherdata: schemas.WeatherDataCreate,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  db_sensor = services.get_sensor_by_sensor_id(db=db, sensor_id=sensor_id)
  if db_sensor is None:
    raise fastapi.HTTPException(
      status_code=400, 
      detail="A sensor with this ID does not exists!"
    )
  return services.create_weatherdata(db=db, weatherdata=weatherdata, sensor_id=sensor_id)


@app.get("/weatherdata/", response_model=List[schemas.WeatherData])
def get_all_weatherdata(
  skip: int = 0,
  limit: int = 50,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  all_weatherdata = services.get_all_weatherdata(db=db, skip=skip, limit=limit)
  return all_weatherdata


@app.put("/weatherdata/{id}/", response_model=schemas.WeatherData)
def update_weatherdata(
  id: int,
  weatherdata: schemas.WeatherDataUpdate,
  db: orm.Session = fastapi.Depends(services.get_db)
):
  return services.update_weatherdata(db=db, id=id, weatherdata=weatherdata)


@app.get("/weatherdatarange/", response_model=List[schemas.WeatherData])
def get_all_weatherdata_in_range(
  db: orm.Session = fastapi.Depends(services.get_db)
):
  weatherdata_in_range = services.get_weatherdata_in_range(db=db)
  return weatherdata_in_range

# GET WEATHERDATA BY Sensorid