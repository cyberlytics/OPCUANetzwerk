from opcua import Client


client = Client('opc.tcp://127.0.0.1:4841')

try:
    client.connect()

    root = client.get_root_node()
    
    objects_folder = root.get_children()[0]
    #print("Objects node has id: ", objects_folder)

    #Sensornetwerk
    sensornetzwerk = objects_folder.get_children()[1]
    #print("Sensornetz node has id: ", sensornetzwerk)

    #Sensorknoten 
    sensornodes = sensornetzwerk.get_children()
    #print("Sensornodes have the ids:",[ i.get_browse_name() for i in sensornodes])

    #Sensoren pro Sensorknoten
    #Liste von Tupeln [ (sensor_name,[sensoren]), ()...  ]
    sensoren = [ (str(node.get_display_name()),node.get_children()) for node in sensornodes]
    for sensor in sensoren:
        print("Sensornode:",sensor[0])
        print("Sensoren:",[ i.get_display_name() for i in sensor[1]])
        print()


finally:
    client.disconnect()