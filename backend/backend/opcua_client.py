from backend import sensor
from backend import actuator
from backend import config

from opcua import Client

class OPCUAClient:
    def __init__(self,opcua_server_uri:str = config.SENSOR_NETWORK_URL):
        self.client = Client(opcua_server_uri)
        try:
            self.client.connect()
            self.sensors ,self.actuators = self.set_sensors_and_actuators() 
        except Exception as e:   
            print(f"Connection to OPCUA Server could not be established, because of {e}")

    def __del__(self):
        self.client.disconnect()

    
    def get_sensor_names(self):
        return [s.get_sensor_name() for s in self.sensors]

    def get_current_sensor_values(self):
        values = [s.get_current_sensor_value() for s in self.sensors]
        return [val for val in values if val is not None]

    def get_sensor_values(self):
        values = [s.get_sensor_value() for s in self.sensors]
        return [val for val in values if val is not None]

    def get_actuator_names(self):
        return [act for act in self.actuators]

    def set_sensors_and_actuators(self):
        #Get a pointer to the "SensorNetwork"-Node starting from root-Node
        root = self.client.get_root_node()
        objects_folder = root.get_children()[0]
        sensornetzwerk = objects_folder.get_children()[1]
        sensornodes = sensornetzwerk.get_children()
        
        #Sensors can be stored in a list, since we can collect data from all of them the same way
        #Actuators are stored in a dict with an Name as a key. This makes them individually reachable
        sensorsObjects = []
        actuatorObjects = {}

        #iterate through each SensorNetwork
        for sensornode in sensornodes:
            #a SensorNode_<ID> has multiple children and we need the "Sensors" and "Actuators" Nodes
            
            for node in sensornode.get_children():
                if node.get_display_name().Text == "Sensors":
                    sensornode_sensors = node
                if node.get_display_name().Text == "Actuators":
                    sensornode_actuators = node
            # add sensors to the list
            if sensornode_sensors:
                sensorsObjects.extend(self.get_all_sensors(sensornode_sensors=sensornode_sensors, sensornode_name=sensornode.get_display_name().Text))
            # add actuators to the dict
            if sensornode_actuators:
                actuatorObjects.update(self.get_all_actuators(sensornode_actuators= sensornode_actuators, sensornode_name=sensornode.get_display_name().Text))

        return sensorsObjects,actuatorObjects


    def get_all_sensors(self,sensornode_sensors, sensornode_name:str):
        """iterate through the Sensors Node inside a SensorNode (SensorNode has an Actuator and a Sensor as children)
        and return the Sensors as BaseSensor-Objects

        Args:
            sensornode_sensors (OPCUA Node): Sensor Node 
            sensornode_name (str): Name of the Sensornode, this is needed as metadata in the BaseSensorObject

        Returns:
            list[Sensor]: Sensors in Node as a list
        """
        sensorObj = []
        for sensor_in_node in sensornode_sensors.get_children():
            for sensorTyp in sensor_in_node.get_children():
                sensorname_param = sensor_in_node.get_display_name().Text
                sensortyp_param = sensorTyp.get_display_name().Text
                
                if sensortyp_param == 'Presence':
                    tempSensor = sensor.PresenceSensor(sensornode = sensornode_name,
                                            sensorname = sensorname_param,
                                            sensortyp = sensortyp_param,
                                            timestampNode = sensorTyp.get_children()[0],
                                            valueNode = sensorTyp.get_children()[1])
                else:                        
                    unitNode = sensorTyp.get_children()[0]
                    valueNode = sensorTyp.get_children()[1]
                    #sometimes unit and value are in a different order, which needs to be swapped
                    if unitNode.get_display_name().Text != "Unit":
                        unitNode, valueNode = valueNode, unitNode
                    tempSensor = sensor.BaseSensor(sensornode = sensornode_name,
                                            sensorname = sensorname_param,
                                            sensortyp = sensortyp_param,
                                            unit = unitNode.get_value(), 
                                            valueNode = valueNode)
                
                sensorObj.append(tempSensor)
        return sensorObj

    def get_all_actuators(self,sensornode_actuators, sensornode_name:str):
        """iterate through the Actuators Node inside a SensorNode (SensorNode has an Actuator and a Sensor as children)
        and return the Actuators as BaseActuator-Objects

        Args:
            sensornode_actuator (OPCUA Node): Actuator Node 
            sensornode_name (str): Name of the Sensornode, this is needed as metadata in the BaseSensorObject

        Returns:
            dict: Key=Names, Values =Actuators
        """
        actuatorDict = {}
        for actuator_node in sensornode_actuators.get_children():
            #create actuatorObject
            act = actuator.create_actuator(actuatorNode = actuator_node, sensornode_name= sensornode_name)
            #insert into dict
            if act:
                actuatorDict[act.get_actuator_name()] = act
        return actuatorDict
    
    def get_controllable_actuators(self,filter_act=None):
        """iterate through actuators and get the controllable parts

        Args:
            filter_act (str, optional): Filter for specific actuator. Defaults to None.

        Returns:
            list of actuator_list_dtos
        """
        act_list = []
        for act_name in self.actuators:
            #check if filter exists
            if filter_act is not None and act_name != filter_act: 
                continue
            act_list.extend(self.actuators[act_name].get_changable_acts())
        return act_list

    def set_actuator_value(self,actuator_node, actuator_act, new_value):
        """pass the command to change the value of an actuator to the actual actuator"""
        try:
            self.actuators[actuator_node].set_changable_act(actuator_act, new_value)
            return True
        except:
            return False
        

opcua_client = OPCUAClient(config.SENSOR_NETWORK_URL)