import pytest
import sqlalchemy as sql
import sqlalchemy.orm as orm
import contextlib
import os
import datetime as dt
from fastapi.testclient import TestClient
from database import Base
from main import app
from services import get_db


##### CREATE TEMPORARY TEST DATABASE FOR UNIT TESTING #####
SQLALCHEMY_TESTDATABASE_URL = "sqlite:///./testdatabase.db"

engine = sql.create_engine(
    SQLALCHEMY_TESTDATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
      db = TestingSessionLocal()
      yield db
    finally:
      db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


##### PYTEST FIXTURES #####
@pytest.fixture()
def sensor_payload():
  return {
    "sensor_id": 1,
    "country": "Ireland",
    "city": "Dublin"
  }

@pytest.fixture()
def weatherdata_payload():
  return {
    "temp": 20,
    "humidity": 60,
    "wind_speed": 40
  }

@pytest.fixture()
def update_weatherdata_payload():
  return {
    "temp": 25,
    "humidity": 55,
    "wind_speed": 45,
    "timestamp": "2022-02-10T09:00:00"
  }


##### Unit Tests #####

def test_homepage():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Yitpin's Code Challenge"}


def test_create_sensor(sensor_payload):
  response = client.post(
    "/sensors/",
    json=sensor_payload
  )
  assert response.status_code == 200
  data = response.json()
  assert data["country"] == "Ireland"
  assert data["city"] == "Dublin"
  assert "sensor_id" in data


def test_sensor_already_exists(sensor_payload):
  response = client.post(
    "/sensors/",
    json=sensor_payload
  )
  assert response.status_code == 400
  data = response.json()
  assert data["detail"] == "A sensor with this ID already exists!"


def test_get_all_sensors(sensor_payload):
  response = client.get(
    "/sensors/"
  )
  assert response.status_code == 200
  data = response.json()
  assert data == [sensor_payload]


def test_get_sensor_by_sensor_id(sensor_payload):
  sensor_id = sensor_payload["sensor_id"]
  response = client.get(
    f"/sensors/{sensor_id}"
  )
  assert response.status_code == 200
  data = response.json()
  assert data == sensor_payload


def test_get_sensor_by_sensor_id_does_not_exist():
  sensor_id = 999
  response = client.get(
    f"/sensors/{sensor_id}"
  )
  assert response.status_code == 400
  data = response.json()
  assert data["detail"] == "A sensor with this ID does not exists!"


def test_create_weatherdata(sensor_payload, weatherdata_payload):
  sensor_id = sensor_payload["sensor_id"]
  response = client.post(
    f"/sensors/{sensor_id}/weatherdata",
    json=weatherdata_payload
  )
  assert response.status_code == 200
  data = response.json()
  assert data["temp"] == 20
  assert data["humidity"] == 60
  assert data["wind_speed"] == 40
  assert "sensor_id" in data


def test_create_weatherdata_sensor_id_does_not_exist(weatherdata_payload):
  sensor_id = 999
  response = client.post(
    f"/sensors/{sensor_id}/weatherdata",
    json=weatherdata_payload
  )
  assert response.status_code == 400
  data = response.json()
  assert data["detail"] == "A sensor with this ID does not exists!"


def test_get_weatherdata_by_sensor_id(sensor_payload):
  sensor_id = sensor_payload["sensor_id"]
  response = client.get(
    f"/sensors/{sensor_id}/weatherdata"
  )
  assert response.status_code == 200
  data = response.json()
  assert data["avg_temp"] == 20
  assert data["avg_humidity"] == 60
  assert data["avg_wind_speed"] == 40
  assert "weatherdata" in data


def test_get_weatherdata_by_sensor_id_does_not_exist():
  sensor_id = 999
  response = client.get(
    f"/sensors/{sensor_id}/weatherdata"
  )
  assert response.status_code == 400
  data = response.json()
  assert data["detail"] == "A sensor with this ID does not exists!"


def test_get_all_weatherdata():
  response = client.get(
    "/weatherdata"
  )
  assert response.status_code == 200
  data = response.json()
  assert data["avg_temp"] == 20
  assert data["avg_humidity"] == 60
  assert data["avg_wind_speed"] == 40
  assert "weatherdata" in data


def test_update_weatherdata(update_weatherdata_payload):
  weatherdata_id = 1
  response = client.put(
    f"weatherdata/{weatherdata_id}/",
    json=update_weatherdata_payload
  )
  assert response.status_code == 200
  data = response.json()
  assert data["temp"] == update_weatherdata_payload["temp"]
  assert data["humidity"] == update_weatherdata_payload["humidity"]
  assert data["wind_speed"] == update_weatherdata_payload["wind_speed"]
  assert data["timestamp"] == update_weatherdata_payload["timestamp"]
  assert "sensor_id" in data


##### DELETE TEST DATABASE AFTER UNIT TESTING #####
def test_delete_testdatase_after_unit_tests():
  """
  Deletes the temporary database after all unit tests are executed so that no data is persisted that will interfere with future unit test runs
  """
  with contextlib.suppress(FileNotFoundError):
    filename = "testdatabase.db"
    os.remove(filename)
    assert True
