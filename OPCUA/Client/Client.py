import sys
import socket
import json
import time
from threading import Thread

from sensors.bme280_sensor import BME280Sensor
from sensors.movement_sensor import MovementSensor
from sensors.mq135 import MQ135

from actors.lcd_display import LcdDisplay

from helpers.systeminformation import SystemInformation
from helpers.opcua_helper import OpcuaHelper
from helpers.opcua_subscription_handler import OpcuaSubscriptionHandler


sys.path.insert(0, "..")


from opcua import Client, ua

# CONSTANTS ---------------------------------
SERVER_ADDRESS         = 'server.sn.local'
OPCUA_PORT             = 4841
# -------------------------------------------

# GLOBAL VARIABLES --------------------------
# -------------------------------------------

def initial_sensornode(sensors):
    sensornode_dict = {
        'BrowseName' : 'SensorNode_',
        'Sensors' : {
            'BME280' : False,
            'HRSR501' : True,
            'KY037' : False,
            'MQ135' : False
        },
        'Actors' : {
            '1602A' : True,
            'LED_Stripe_1' : True,
            'Piezo_1' : True
        }
    }

    for sensor in sensors.values():
        if(type(sensor) == BME280Sensor):
            if (sensor.temperature != None and sensor.humidity != None and sensor.airpressure != None):
                sensornode_dict["Sensors"]["BME280"] = True

        if(type(sensor) == SystemInformation):
            sensornode_dict["BrowseName"] += sensor.hostname[-1]

    send_sensornode_information(sensornode_dict)

def send_sensornode_information(sensornode_dict):
    # Initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.60.11', 8080))

    # Send sensor structure
    sock.send(json.dumps(sensornode_dict).encode('utf-8'))

    # Close socket
    sock.close()

def measurement_thread(sensors, opc):
    while True:
        for sensor in sensors:
            if isinstance(sensor, BME280Sensor):
                temperature = None
                humidity = None
                airpressure = None
                try:
                    temperature = sensor.temperature
                    humidity = sensor.humidity
                    airpressure = sensor.airpressure
                    opc.write_value('Temperature', 'Value', temperature[0])
                    opc.write_value('Humidity', 'Value', humidity[0])
                    opc.write_value('AirPressure', 'Value', airpressure[0])
                except Exception as ex:
                    print(f'Reading of BME280 values error: {ex}')

            if type(sensor) == MQ135:
                pass

        time.sleep(3)


if __name__ == "__main__":
    client = Client(f"opc.tcp://{SERVER_ADDRESS}:{OPCUA_PORT}")

    try:
        client.connect()   
    except Exception as ex:
        print(f'Opcua Client connect: {ex}')
        exit()

    # Initialize sensors
    sensors = []
    bme280 = BME280Sensor(0x77)
    sensors.append(bme280)
    movement_sensor = MovementSensor(17)
    sensors.append(movement_sensor)

    # Initialize helpers
    systeminformation = SystemInformation()

    # Initialize actors
    actors = []
    lcd = LcdDisplay()
    actors.append(lcd)

    # Initialize OPCUA
    opc = OpcuaHelper(client, systeminformation.hostname[-1])

    # Initial read
    #initial_sensornode(sensors)
    
    # Start measurement thread
    t = Thread(target=measurement_thread, args=[sensors, opc])
    t.start()

    # Function for updating mov

    # Update of movement sensor
    def update_movement_sensor(sender, args):
        try:
            opc.write_value('Presence', 'Value', args['new'])
            opc.write_value('Presence', 'Timestamp', time.time())
        except Exception as ex:
            print(f'Opcua Write Value: {ex}')
    movement_sensor.PresenceChanged.subscribe(update_movement_sensor)
    movement_sensor.start_measurement()

    # Do other stuff
    lcd.set_backlight(True)
    lcd.text = ('ABC', 'DEF')

    def testfunc(sender, args):
        print(args)

        if args['new'] == None:
            return

        line = str(args['node']).split('.')[-1]
        text = list(lcd.text)
        if line == 'TextLine1':
            text[0] = args['new'].ljust(16)
        elif line == 'TextLine2':
            text[1] = args['new'].ljust(16)
        lcd.text = text

    
    node1 = client.get_node('ns=2;s=SensorNode_2.Actuators.1602A.TextLine1')
    node2 = client.get_node('ns=2;s=SensorNode_2.Actuators.1602A.TextLine2')

    handler = OpcuaSubscriptionHandler()
    handler.DataChanged.subscribe(testfunc)

    sub = client.create_subscription(500, handler)
    sub.subscribe_data_change(node1)
    sub.subscribe_data_change(node2)

    