from opcua import Client, ua
from threading import Thread
import time

class OpcuaHelper(object):
    def __init__(self, clientHandle, sensornode_number):
        self.__client = clientHandle
        self.__set_connected(True)

        # Get all important nodes from server
        self.__sensornode_node = self.__client.get_node(f'ns=2;s=SensorNode_{sensornode_number}')
        self.__get_sensors()
        self.__get_actors()
        self.__get_hw_os_attributes()

    def opcua_server_reachable(self):
        try:
            self.__client.get_root_node()
        except Exception as ex:
            print(f"No connection to opcua Server: {ex}")
            self.__set_connected(False)
            return False

        return True

    def reconnect_to_server(self):
        i = 0
        while True:
            if i < 5:
                timeout = 60
            else:
                timeout = 1200
            try:
                self.__client.connect()
                self.Connected = True
                break
            except Exception as ex:
                print(f'Reconnect {i} to opcua Server failed: {ex}')
                    
            i += 1
            time.sleep(timeout)


    def __get_sensors(self):
        for subnode in self.__sensornode_node.get_children():
            if subnode.get_browse_name().Name == "Sensors":
                self.__sensor_nodes = subnode.get_children()

    def __get_actors(self):
        for subnode in self.__sensornode_node.get_children():
            if subnode.get_browse_name().Name == "Actuators":
                self.__actor_nodes = subnode.get_children()

    def __get_hw_os_attributes(self):
        self.__hw_os_attributes = []
        for subnode in self.__sensornode_node.get_children():
            if subnode.get_browse_name().Name == "HardwarePlatform":
                self.__hw_os_attributes.append(subnode)
                # If value node then add it
                for childnode in subnode.get_children():
                    ## If object node, then add its children
                    if childnode.get_node_class() == ua.NodeClass.Object:
                        self.__hw_os_attributes.append(childnode)



    def write_value(self, nodename, attribute, value):
        node = self.__get_node(nodename)
        attribute_node = self.__get_attribute_node(node, attribute)
        attribute_node.set_value(value)


    def __get_node(self, nodename):
        for subnode in self.__sensor_nodes + self.__actor_nodes + self.__hw_os_attributes:
            if subnode.get_browse_name().Name == nodename:
                return subnode
            for childnode in subnode.get_children():
                if childnode.get_browse_name().Name == nodename:
                    return childnode

        print(f'Node "{nodename}" not found')


    def __get_attribute_node(self, node, attribute):
        for subnode in node.get_children():
            if subnode.get_browse_name().Name == attribute:
                return subnode

        print(f'Attribute "{attribute}" not found in Node: "{node.get_browse_name().Name}"')

    @property
    def Connected(self):
        return self.__connected
    def __set_connected(self, new_value):
        self.__connected = new_value