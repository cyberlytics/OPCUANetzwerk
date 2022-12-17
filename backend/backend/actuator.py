from typing import Protocol
from opcua import Client


class A_1602A:
    def __init__(self,node,sensornode_name):
        self.sensornode= sensornode_name
        self.sensor_descriptor= node.get_display_name().Text
        self.node = node

    def get_actuator_name(self):
        return f'{self.sensornode}-{self.sensor_descriptor}'

class LED_Stripe:
    def __init__(self,node,sensornode_name):
        self.sensornode= sensornode_name
        self.sensor_descriptor= node.get_display_name().Text
        self.node = node

    def get_actuator_name(self):
        return f'{self.sensornode}-{self.sensor_descriptor}'

class Piezo:
    def __init__(self,node,sensornode_name):
        self.sensornode= sensornode_name
        self.sensor_descriptor= node.get_display_name().Text
        self.node = node

    def get_actuator_name(self):
        return f'{self.sensornode}-{self.sensor_descriptor}'

def create_actuator(actuatorNode,sensornode_name:str):
    actTyp = actuatorNode.get_display_name().Text
    
    if actTyp == "1602A": 
        return A_1602A(node=actuatorNode,sensornode_name=sensornode_name)

    if actTyp.startswith("LED_Stripe_"):
        return LED_Stripe(node=actuatorNode,sensornode_name=sensornode_name)
    
    if actTyp.startswith("Piezo_1"):
        return Piezo(node=actuatorNode,sensornode_name=sensornode_name)

    
    