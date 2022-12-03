from opcua import Client
from datetime import datetime

class Sensor:

    def __init__(self, sensornode, sensorname, sensortyp, unit, valueNode):
        self.sensornode = sensornode
        self.sensorname = sensorname
        self.sensortyp = sensortyp
        self.unit = unit
        self.valueNode = valueNode
        
    def getSensorValue(self):
        return { 
            "sensornode": self.sensornode,
            "sensorname": self.sensorname,
            "sensortyp": self.sensortyp,
            "unit": self.unit,
            "value": self.valueNode.get_value(),
            "timestamp": datetime.now().isoformat()
            }
