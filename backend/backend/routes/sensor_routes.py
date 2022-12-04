from fastapi import APIRouter, Response,status,Request

from backend.models.sensorValueDto import SensorValueDto
from backend.database import conn
from backend import config
from backend.opcua_client import opcua_client

router_sensors = APIRouter()
db_sensors = conn[config.DB_NAME].sensors

@router_sensors.get('/sensornames',tags=['Sensors'])
async def get_sensor_names():
    """Return an example JSON to test structure of app"""
    return opcua_client.get_sensor_names()

@router_sensors.get('/sensorvalues',tags=['Sensors'], response_model=list[SensorValueDto])
async def get_all_sensor_values():
    """Return an example JSON to test structure of app"""
    return opcua_client.get_sensor_values()