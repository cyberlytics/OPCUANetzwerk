import uvicorn
from backend import config
from backend.database import conn
from backend.opcua_client import opcua_client, OPCUAClient
from backend.routes.sensor_routes import db_sensors
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from backend import app


@app.on_event("startup")
@repeat_every(seconds=config.COLLECT_TIMEWINDOW_SECONDS)
def collect_and_insert_data():
    sensor_values = opcua_client.get_sensor_values()
    db_sensors.insert_many(sensor_values)

@app.on_event("startup")
@repeat_every(seconds=config.COLLECT_TIMEWINDOW_SECONDS)
def refresh_opcua_client():
    opcua_client = OPCUAClient(config.SENSOR_NETWORK_URL)

@app.on_event("startup")
@repeat_every(seconds=config.COLLECT_TIMEWINDOW_SECONDS)
def update_act_values():
    opcua_client.update_current_act_values()

uvicorn.run('backend:app', host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL)