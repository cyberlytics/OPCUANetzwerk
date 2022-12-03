from opcua import Client
from datetime import datetime

class Sensor:
    """Wrapper for a sensor and all of his meta data"""
    def __init__(self, sensornode:str, sensorname:str, sensortyp:str, unit:str, valueNode:str):
        self.sensornode = sensornode
        self.sensorname = sensorname
        self.sensortyp = sensortyp
        self.unit = unit
        self.valueNode = valueNode
        
    def getSensorValue(self):
        """Get the current value of sensor + additional meta as a dict """
        try:
            return { 
            "sensornode": self.sensornode,
            "sensorname": self.sensorname,
            "sensortyp": self.sensortyp,
            "unit": self.unit,
            "value": self.valueNode.get_value(),
            "timestamp": datetime.now().isoformat()
            }
        except: 
            print("Could not get Value for sensor: ", self.sensorname)
    
    def get_sensor_name(self):
        return f'{self.sensornode}-{self.sensorname}-{self.sensortyp}'