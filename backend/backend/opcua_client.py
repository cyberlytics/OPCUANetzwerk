from opcua import Client
import sensor


client = Client('opc.tcp://127.0.0.1:4841')

try:
    client.connect()

    root = client.get_root_node()
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
    print("Sensor: ", sensorObj[0].getSensorValue())

finally:
    client.disconnect()