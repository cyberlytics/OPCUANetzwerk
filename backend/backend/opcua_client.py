from backend import sensor
from backend import config

from opcua import Client

class OPCUAClient:
    def __init__(self,opcua_server_uri:str = config.SENSOR_NETWORK_URL):
        self.client = Client(opcua_server_uri)
        self.sensors = self.get_all_sensors()

    def __del__(self):
        self.client.disconnect()

    def get_all_sensors(self):
        """iterate through the OPCUA Server and collect all the sensors

        Returns:
            list[Sensor]: All Sensors in OPCUA Server as a list
        """
        self.client.connect()
        root = self.client.get_root_node()
        objects_folder = root.get_children()[0]
        sensornetzwerk = objects_folder.get_children()[1]
        sensornodes = sensornetzwerk.get_children()

        sensorObj = []
        #creating a sensor object for each sensor
        for sensornode in sensornodes:
            for sensor_in_node in sensornode.get_children():
                for sensorTyp in sensor_in_node.get_children():
                    tempSensor = sensor.Sensor(sensornode = sensornode.get_display_name().Text,
                                                sensorname = sensor_in_node.get_display_name().Text,
                                                sensortyp = sensorTyp.get_display_name().Text,
                                                unit = sensorTyp.get_children()[0].get_value(), 
                                                valueNode = sensorTyp.get_children()[1])
                    sensorObj.append(tempSensor)
        return sensorObj
    
    def get_sensor_names(self):
        return [s.get_sensor_name() for s in self.sensors]

    def get_sensor_values(self):
        return [s.get_sensor_value() for s in self.sensors if s.get_sensor_value() is not None]

opcua_client = OPCUAClient(config.SENSOR_NETWORK_URL)