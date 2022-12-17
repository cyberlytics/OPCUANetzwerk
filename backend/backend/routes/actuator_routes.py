from fastapi import APIRouter, Response,status,Request
import datetime

from backend import config
from backend.opcua_client import opcua_client

router_actuators = APIRouter()

@router_actuators.get('/actuatornames',tags=['Actuators'])
async def get_actuator_names():
    """Return an list with all available sensors"""
    return opcua_client.get_actuator_names()