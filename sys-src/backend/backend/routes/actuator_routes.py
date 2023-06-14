from fastapi import APIRouter, Response,status,Request
import datetime

from backend import config
from backend.opcua_client import opcua_client
from backend.models.actuators_dto import actuator_list_dto, actuator_change_dto

router_actuators = APIRouter()

@router_actuators.get('/actuatornames',tags=['Actuators'],response_model=list[str])
async def get_actuator_names():
    """Return an list with all available sensors"""
    return opcua_client.get_actuator_names()

@router_actuators.get('/actuators',tags=['Actuators'],response_model=list[actuator_list_dto])
async def get_controllable_actuators():
    return opcua_client.get_controllable_actuators(filter_act=None)

@router_actuators.get('/actuators/{filter_by_actuatorname}',tags=['Actuators'],response_model=list[actuator_list_dto])
async def get_controllable_actuators_with_filter(filter_by_actuatorname:str):
    return opcua_client.get_controllable_actuators(filter_act=filter_by_actuatorname)

@router_actuators.put('/actuators',tags=['Actuators'])
async def set_actuator_value(body: actuator_change_dto, response:Response):
    success = opcua_client.set_actuator_value(actuator_node = body.actuator_node,
                                            actuator_act = body.actuator_act,
                                            new_value = body.new_value)
    if not success: 
        response.status_code = status.HTTP_400_BAD_REQUEST