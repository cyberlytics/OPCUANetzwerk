from opcua import Client
import datetime

class BaseSensor:
    """Wrapper for a sensor and all of his meta data"""
    def __init__(self, sensornode:str, sensorname:str, sensortyp:str, unit:str, valueNode):
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
                "timestamp": datetime.datetime.now()#.isoformat()
                }
            else:
                print("Value for sensor: ", self.get_sensor_name() + "was null - This seems suspicious!")
        except: 
            print("Could not get Value for sensor: ", self.get_sensor_name())
    
    
    def get_current_sensor_value(self):
        """The API endpoint for current sensor values calls this function. For Base sensors this is identical to the get_sensor_value() method"""
        return self.get_sensor_value()

    def get_sensor_name(self):
        return f'{self.sensornode}-{self.sensorname}-{self.sensortyp}'


class PresenceSensor:
    """Wrapper for a presence sensor and all of his meta data"""
    def __init__(self, sensornode:str, sensorname:str, sensortyp:str,timestampNode):
        self.sensornode = sensornode
        self.sensorname = sensorname
        self.sensortyp = sensortyp
        self.timestampNode = timestampNode
        #timestamp is in seconds from 1970
        self.last_timestamp = None

    def get_sensor_value(self):
        """Return last timestamp if it wasn't already returned"""
        last_measure = self.get_current_sensor_timestamp()
        print(last_measure)
        #if last_measure == last_timestamp means that the measure was already present
        if last_measure['timestamp'] != self.last_timestamp:
            self.last_timestamp = last_measure['timestamp']
            print('here')
            return last_measure
    
    def get_current_sensor_value(self):
        """Returns the last timestamp where presence was measured"""
        return { 
            "sensornode": self.sensornode,
            "sensorname": self.sensorname,
            "sensortyp": self.sensortyp,
            "value": True,
            "timestamp": datetime.datetime.utcfromtimestamp(self.timestampNode.get_value())
            }

    def get_sensor_name(self):
        return f'{self.sensornode}-{self.sensorname}-{self.sensortyp}'