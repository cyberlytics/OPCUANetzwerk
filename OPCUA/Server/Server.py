#!/usr/bin/python

from opcua import Server, instantiate, ua, Client
import time
from threading import Thread
import socket
import json
from pathlib import Path

# CONSTANTS ---------------------------------
SERVER_ADDRESS         = 'server.sn.local'
OPCUA_PORT             = 4841
SENSORNETWORK_NODEID   = 'ns=2;i=1036'
SENSORNODE_TYPE_NODEID = 'ns=2;i=1009'
INFORMATION_MODEL      = 'Informationsmodell.xml'
# -------------------------------------------

def threadFunc(serverHandle):
    time.sleep(5)
    sensornetwork_node = serverHandle.get_node('ns=2;i=1036')
    
    airpressure = 1000
    humidity = 40
    temperature = 5
    airquality = 400
    
    while True:
        time.sleep(10)
        
        airpressure = airpressure + 1.1
        if airpressure > 1050:
            airpressure = 1000
        
        humidity = humidity + 1
        if humidity > 80:
            humidity = 40
        
        temperature = temperature + 1
        if temperature > 40:
            temperature = 5
        
        airquality = airquality + 10
        if airquality > 2200:
            airquality = 400
    
        # Quick and dirty way to iterate over everything
        for sensornode in sensornetwork_node.get_children():
            for sensor in sensornode.get_children():
                for sensorvalue in sensor.get_children():
                    for sensorattribute in sensorvalue.get_children():
                    
                        # Set AirPressure
                        if sensorvalue.get_browse_name() == ua.QualifiedName('AirPressure', 2) and\
                            sensorattribute.get_browse_name() == ua.QualifiedName('Value', 2):
                                sensorattribute.set_value(airpressure)
                                
                        # Set Humidity
                        if sensorvalue.get_browse_name() == ua.QualifiedName('Humidity', 2) and\
                            sensorattribute.get_browse_name() == ua.QualifiedName('Value', 2):
                                sensorattribute.set_value(humidity)
                                
                        # Set Temperature
                        if sensorvalue.get_browse_name() == ua.QualifiedName('Temperature', 2) and\
                            sensorattribute.get_browse_name() == ua.QualifiedName('Value', 2):
                                sensorattribute.set_value(temperature)
                                
                        # Set AirQuality
                        if sensorvalue.get_browse_name() == ua.QualifiedName('AirQuality', 2) and\
                            sensorattribute.get_browse_name() == ua.QualifiedName('Value', 2):
                                sensorattribute.set_value(airquality)
                        
    time.sleep(30)
    
    serverHandle.stop()
    exit()
        
def sock_thread(opcua_server_handle):

    # Create and bind socket
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('192.168.60.11', 8080))
    
    # Listen for new connections
    serv.listen(5)
    while True:

        # New client is connected
        conn, addr = serv.accept()

        # Read data
        data = conn.recv(4096)
        msg = data.decode('utf-8')
        
        # Convert received data back to dictionary
        sensornode_dict = json.loads(msg)
        handle_client(opcua_server_handle, sensornode_dict)

        # Close connection
        conn.close()

def handle_client(server, client_dict):
    sensornetwork_node = server.get_node(SENSORNETWORK_NODEID)
    sensornode_type = server.get_node(SENSORNODE_TYPE_NODEID)

    # Get current sensornodes
    sensornode_names = [node.get_browse_name().Name for node in sensornetwork_node.get_children()]
    
    # If new sensornode is already in the information model do nothing. Otherwise add it
    sensornode_name = client_dict["BrowseName"]
    if sensornode_name not in sensornode_names:

        # Add new child node with sensnornode_type
        sensornode = sensornetwork_node.add_object(f'ns=2;s={sensornode_name}', sensornode_name, sensornode_type.nodeid)
        
        # Iterate children of added sensornode and delete missing sensors
        # This is a dirty way, but the opcua-python library does instantiate
        # all children, even if modelling rule is set to optional
        sensors = [sensor for sensor in client_dict["Sensors"].keys() if client_dict["Sensors"][sensor]]

        for subnode in sensornode.get_children():
            if subnode.get_browse_name().Name == 'Sensors':
                for sensor in subnode.get_children():
                    if sensor.get_browse_name().Name not in sensors:
                        sensor.delete()


if __name__ == "__main__":

    # Create Server Object
    server = Server()
    
    # Set Endpoint, import information model and start server
    server.set_endpoint(f"opc.tcp://{SERVER_ADDRESS}:{OPCUA_PORT}")
    server.import_xml(Path(__file__).parent.joinpath(INFORMATION_MODEL))
    server.start()

    # Start thread to handle new clients
    t = Thread(target=sock_thread, args=[server])
    t.start()



