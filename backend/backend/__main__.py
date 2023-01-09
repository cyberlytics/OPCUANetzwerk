import uvicorn
from backend import config
from backend.database import conn
from backend.opcua_client import opcua_client
from backend.routes.sensor_routes import db_sensors
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from backend import app
from opcua_client import OPCUAClient


@app.on_event("startup")
@repeat_every(seconds=config.COLLECT_TIMEWINDOW_SECONDS)
def collect_and_insert_data():
    sensor_values = opcua_client.get_sensor_values()
    db_sensors.insert_many(sensor_values)

uvicorn.run('backend:app', host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL)