from opcua import Server, ua
import time
from threading import Thread

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
        

if __name__ == "__main__":

    server = Server()

    t = Thread(target=threadFunc, args=[server])
    t.start()
    
    server.set_endpoint("opc.tcp://127.0.0.1:4841")
    server.import_xml("Informationsmodell.xml")
    server.start()