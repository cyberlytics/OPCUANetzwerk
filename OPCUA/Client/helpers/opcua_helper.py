from opcua import Client, ua

class OpcuaHelper(object):
    def __init__(self, clientHandle, sensornode_number):
        self.__client = clientHandle
        self.__sensornode_node = self.__client.get_node(f'ns=2;s=SensorNode_{sensornode_number}')
        self.__get_sensors()
        self.__get_actors()
        self.__get_hw_os_attributes()


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
                # If value node then add it
                for childnode in subnode.get_children():
                    if childnode.get_node_class() == ua.NodeClass.Variable:
                        self.__hw_os_attributes.append(childnode)

                    ## If object node, then search its children
                    if childnode.get_node_class() == ua.NodeClass.Object:
                        for attribute_node in childnode.get_children():
                            if attribute_node.get_node_class() == ua.NodeClass.Variable:
                                self.__hw_os_attributes.append(childnode)



    def write_value(self, nodename, attribute, value):
        node = self.__get_node(nodename)
        attribute_node = self.__get_attribute_node(node, attribute)
        attribute_node.set_value(value)


    def __get_node(self, nodename):
        for subnode in self.__sensor_nodes + self.__actor_nodes:
            for childnode in subnode.get_children():
                if childnode.get_browse_name().Name == nodename:
                    return childnode

        print(f'Node "{nodename}" not found')


    def __get_attribute_node(self, node, attribute):
        for subnode in node.get_children():
            if subnode.get_browse_name().Name == attribute:
                return subnode

        print(f'Attribute "{attribute}" not found in Node: "{node.get_browse_name().Name}"')