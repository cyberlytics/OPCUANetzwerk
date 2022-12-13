from fastapi import APIRouter, Response,status,Request
import datetime

from backend.models.sensor_value_dto import Sensor_value_dto
from backend.database import conn
from backend import config
from backend.opcua_client import opcua_client

router_sensors = APIRouter()
db_sensors = conn[config.DB_NAME].sensors

@router_sensors.get('/sensornames',tags=['Sensors'])
async def get_sensor_names():
    """Return an list with all available sensors"""
    return opcua_client.get_sensor_names()

@router_sensors.get('/sensorvalues/current',tags=['Sensors'], response_model=list[Sensor_value_dto])
async def get_current_sensor_values():
    """Return current value for each sensor"""
    return opcua_client.get_sensor_values()

@router_sensors.get('/sensorvalues', tags=['Sensors'], response_model=list[Sensor_value_dto])
async def get_sensor_values_with_filter(sensornode:str = None, 
        sensorname:str = None, 
        sensortyp:str=None,
        startTimestamp:datetime.datetime = None, 
        endTimestamp:datetime.datetime = None):
    """Return sensor values filtered for time and other attributes"""
    #create a dict with filters which were provided as query parameters
    filter_dict = {}
    for field_value,field_name in zip([sensornode,sensorname, sensortyp],['sensornode','sensorname','sensortyp']):
        if field_value is not None:
            filter_dict[field_name] = field_value

    #if no time provided -> doint filter for time
    time_filter = {}
    if startTimestamp is not None:
        time_filter['$gte']=startTimestamp
    if endTimestamp is not None:
        time_filter['$lt']=endTimestamp
    #add to filter dict if not empty
    if time_filter:
        filter_dict['timestamp']=time_filter
    
    return [datapoint for datapoint in db_sensors.find(filter_dict,{"_id":0})]