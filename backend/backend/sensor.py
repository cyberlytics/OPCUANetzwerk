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
        
    def get_sensor_value(self):
        """Get the current value of sensor + additional meta as a dict """
        try:
            value = self.valueNode.get_value()
            if(value):
                return { 
                "sensornode": self.sensornode,
                "sensorname": self.sensorname,
                "sensortyp": self.sensortyp,
                "unit": self.unit,
                "value": value,
                "timestamp": datetime.now().isoformat()
                }
            else:
                print("Value for sensor: ", self.get_sensor_name() + "was null - This seems suspicious!")
        except: 
            print("Could not get Value for sensor: ", self.get_sensor_name())
    
    def get_sensor_name(self):
        return f'{self.sensornode}-{self.sensorname}-{self.sensortyp}'