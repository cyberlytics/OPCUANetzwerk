#!/usr/bin/python

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
import helpers.globals as globals

sys.path.insert(0, "..")

from opcua import Client, ua

def initialize_sensornode():
    sensornode_dict = {
        'BrowseName' : 'SensorNode_' + globals.sys_info.hostname[-1],
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
    send_sensornode_information(sensornode_dict)

def send_sensornode_information(sensornode_dict):
    # Initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.60.11', 8080))

    # Send sensor structure
    sock.send(json.dumps(sensornode_dict).encode('utf-8'))

    # Close socket
    sock.close()

def measurement_thread():
    temperature = None
    humidity = None
    airpressure = None
    airquality = None
    while True:
        # BME280
        try:
            temperature = globals.bme280.temperature
            humidity = globals.bme280.humidity
            airpressure = globals.bme280.airpressure
        except Exception as ex:
            print(f'Reading of BME280 values error: {ex}')

        # MQ135
        if temperature != None and humidity != None:
            try:
                airquality = globals.mq135.get_corrected_ppm(temperature[0], humidity[0])
            except Exception as ex:
                print(f'Getting Air Quality failed: {airquality}')

        print('-----------------------------------------------')
        print(f'Temperatur:       {temperature[0]:.2f} C')
        print(f'Luftfeuchtigkeit: {humidity[0]:.2f} %')
        print(f'Lufdruck:         {airpressure[0]:.2f} hPa')
        print(f'CO2-Gehalt:       {airquality:.2f} ppm')

        # Set LEDS according to air value
        if airquality < globals.AirQuality.WarningLevel:
            globals.led_stripe.green_on()
        if airquality > globals.AirQuality.WarningLevel and airquality < globals.AirQuality.AlarmLevel:
            globals.led_stripe.orange_on()
        if airquality > globals.AirQuality.AlarmLevel:
            globals.led_stripe.red_on()

        ## Write values to pcua
        #try:
        #    globals.opc.write_value('Temperature', 'Value', temperature[0])
        #    globals.opc.write_value('Humidity', 'Value', humidity[0])
        #    globals.opc.write_value('AirPressure', 'Value', airpressure[0])
        #except Exception as ex:
        #    print(f'Writing sensor_value to opcua_server error: {ex}')


        time.sleep(3)

def status_led_thread():
    while True:
        print(globals.connection_helper.Status)
        print('----------------------')
        if globals.connection_helper.Status == globals.connection_helper.OK:
            globals.led_stripe.BlueLED.Short_Blink(globals.connection_helper.OK)
        if globals.connection_helper.Status == globals.connection_helper.OPCUA_SERVER_NOT_REACHABLE:
            globals.led_stripe.BlueLED.Short_Blink(globals.connection_helper.OPCUA_SERVER_NOT_REACHABLE)
        if globals.connection_helper.Status == globals.connection_helper.SERVER_NODE_NOT_REACHABLE:
            globals.led_stripe.BlueLED.Short_Blink(globals.connection_helper.SERVER_NODE_NOT_REACHABLE)
        if globals.connection_helper.Status == globals.connection_helper.VPN_GATEWAY_NOT_REACHABLE:
            globals.led_stripe.BlueLED.Short_Blink(globals.connection_helper.VPN_GATEWAY_NOT_REACHABLE)
        if globals.connection_helper.Status == globals.connection_helper.NO_INTERNET_CONNECTION:
            globals.led_stripe.BlueLED.Short_Blink(globals.connection_helper.NO_INTERNET_CONNECTION)

        time.sleep(2.5)

def init_movement_sensor():
    def update_movement_sensor(sender, args):
        try:
            globals.opc.write_value('Presence', 'Value', args['new'])
            globals.opc.write_value('Presence', 'Timestamp', time.time())
        except Exception as ex:
            print(f'Opcua Write Value: {ex}')
    globals.movement_sensor.PresenceChanged.subscribe(update_movement_sensor)
    globals.movement_sensor.start_measurement()

def init_lcd_update():
    def update_opcua_screen(sender, args):
        if args['new'] == None:
            return

        # Get last element of node id
        line = str(args['node']).split('.')[-1]

        # Get current text for opcua screen and update the correct line
        text = globals.lcd.get_screen('opcua')['Text']
        if line == 'TextLine1':
            text[0] = args['new'].ljust(16)
        elif line == 'TextLine2':
            text[1] = args['new'].ljust(16)
        globals.lcd.change_screen_text('opcua', text)

    node1 = globals.opcua_client.get_node(f'ns=2;s=SensorNode_{globals.sys_info.hostname[-1]}.Actuators.1602A.TextLine1')
    node2 = globals.opcua_client.get_node(f'ns=2;s=SensorNode_{globals.sys_info.hostname[-1]}.Actuators.1602A.TextLine2')

    handler = OpcuaSubscriptionHandler()
    handler.DataChanged.subscribe(update_opcua_screen)

    sub = globals.opcua_client.create_subscription(500, handler)
    sub.subscribe_data_change(node1)
    sub.subscribe_data_change(node2)

if __name__ == "__main__":
    #time.sleep(30)

    globals.init()

    # Initialize sensornode --> call server and setup nodes
    #initialize_sensornode()
    
    # Start measurement thread
    t = Thread(target=measurement_thread, args=[])
    t.start()

    # Thread for status LED
    t2 = Thread(target=status_led_thread, args=[])
    t2.start()

    # Initialize everything for movement sensor
    #init_movement_sensor()

    # Update
    #init_lcd_update()

    # Delete Me