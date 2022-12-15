from backend import sensor
from backend import config

from opcua import Client

class OPCUAClient:
    def __init__(self,opcua_server_uri:str = config.SENSOR_NETWORK_URL):
        self.client = Client(opcua_server_uri)
        self.sensors = self.get_all_sensors()
        self.actuators = self.get_all_actuators()

    def __del__(self):
        self.client.disconnect()

    def get_all_actuators(self):
        """iterate through the OPCUA Server and collect all the actuators

        Returns: 
            list[Actuators]: All Actuators in OPCUA Server as a list
        """
        return []

    def get_all_sensors(self):
        """iterate through the OPCUA Server and collect all the sensors

        Returns:
            list[Sensor]: All Sensors in OPCUA Server as a list
        """
        try:
            self.client.connect()
            root = self.client.get_root_node()
            objects_folder = root.get_children()[0]
            sensornetzwerk = objects_folder.get_children()[1]
            sensornodes = sensornetzwerk.get_children()

            sensorObj = []
            #creating a sensor object for each sensor
            for sensornode in sensornodes:
                sensornode_sensors = sensornode.get_children()[0]
                sensornode_actuators = sensornode.get_children()[1]
                
                for sensor_in_node in sensornode_sensors.get_children():
                    for sensorTyp in sensor_in_node.get_children():
                        sensornode_param = sensornode.get_display_name().Text
                        sensorname_param = sensor_in_node.get_display_name().Text
                        sensortyp_param = sensorTyp.get_display_name().Text
                        
                        if sensortyp_param == 'Presence':
                            tempSensor = sensor.PresenceSensor(sensornode = sensornode_param,
                                                    sensorname = sensorname_param,
                                                    sensortyp = sensortyp_param,
                                                    timestampNode = sensorTyp.get_children()[0])
                        else:                        
                            unitNode = sensorTyp.get_children()[0]
                            valueNode = sensorTyp.get_children()[1]
                            #sometimes unit and value are in a different order, which needs to be swapped
                            if unitNode.get_display_name().Text != "Unit":
                                unitNode, valueNode = valueNode, unitNode
                            tempSensor = sensor.BaseSensor(sensornode = sensornode_param,
                                                    sensorname = sensorname_param,
                                                    sensortyp = sensortyp_param,
                                                    unit = unitNode.get_value(), 
                                                    valueNode = valueNode)
                        
                        sensorObj.append(tempSensor)
            return sensorObj
        except Exception as e:   
            print(f"Connection to OPCUA Server could not be established, because of {e}")
            return []
    
    def get_sensor_names(self):
        return [s.get_sensor_name() for s in self.sensors]

    def get_current_sensor_values(self):
        values = [s.get_current_sensor_value() for s in self.sensors]
        return [val for val in values if val is not None]

    def get_sensor_values(self):
        values = [s.get_sensor_value() for s in self.sensors]
        return [val for val in values if val is not None]

opcua_client = OPCUAClient(config.SENSOR_NETWORK_URL)