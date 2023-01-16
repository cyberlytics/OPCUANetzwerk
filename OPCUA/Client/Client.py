#!/usr/bin/python

from sqlite3 import connect
from opcua import Client
from threading import Thread
import smbus2, time, sys, socket, json

from libs.extension import Microcontroller, RefVoltage, Prescaler

from helpers.airquality import AirQuality
from helpers.opcua_helper import OpcuaHelper
from helpers.systeminformation import SystemInformation
from helpers.connection_helper import ConnectionHelper
from helpers.opcua_subscription_handler import OpcuaSubscriptionHandler
from helpers.template_string import TemplateString
from helpers.menu import Menu
from helpers.music_helper import MusicHelper

from sensors.bme280_sensor import BME280Sensor
from sensors.mq135 import MQ135
from sensors.movement_sensor import MovementSensor

from actors.lcd_display import LcdDisplay
from actors.led_stripe import LedStripe
from actors.piezo import Piezo

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

# CONSTANTS ---------------------------------
SERVER_ADDRESS         = 'server.sn.local'
OPCUA_PORT             = 4841
VERBOSE                = False
# -------------------------------------------

# Verbose printing
vprint = print if VERBOSE else lambda *a, **k: None

# SensorNode Initiliaze
def initialize_sensornode(node_number):
    sensornode_dict = {
        'BrowseName' : f'SensorNode_{node_number}',
        'Sensors' : {
            'BME280' : True,
            'HRSR501' : True,
            'KY037' : False,
            'MQ135' : True
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

# Measurement Thread
def measurement_thread(args):
    lcd = args['lcd']
    bme280 = args['bme280']
    mq135 = args['mq135']

    lcd.add_screen('sensor1' , ('',''))
    lcd.add_screen('sensor2', ('',''))

    temperature = None
    humidity = None
    airpressure = None
    airquality = None
    while True:
        # BME280
        try:
            temperature = bme280.temperature
            humidity    = bme280.humidity
            airpressure = bme280.airpressure
        except Exception as ex:
            print(f'Reading of BME280 values error: {ex}')

        # MQ135
        if temperature[0] != None and humidity[0] != None:
            try:
                airquality = mq135.get_corrected_ppm(temperature[0], humidity[0])
            except Exception as ex:
                print(f'Getting Air Quality failed: {ex}')

        if temperature[0] != None and humidity[0] != None and airpressure[0] != None and airquality != None:
            vprint('-----------------------------------------------')
            vprint(f'Temperatur:       {temperature[0]:.2f} C')
            vprint(f'Luftfeuchtigkeit: {humidity[0]:.2f} %')
            vprint(f'Lufdruck:         {airpressure[0]:.2f} hPa')
            vprint(f'CO2-Gehalt:       {airquality:.2f} ppm')

        # Set LEDS according to air value
        led_red     = False
        led_orange  = False
        led_green   = False

        if airquality != None:
            if airquality < AirQuality.WarningLevel:
                led_stripe.green_on()
                led_green = True
                piezo.stop_alarm()
            if airquality > AirQuality.WarningLevel and airquality < AirQuality.AlarmLevel:
                led_stripe.orange_on()
                led_orange = True
                piezo.stop_alarm()
            if airquality > AirQuality.AlarmLevel:
                led_stripe.red_on()
                led_red = True
                piezo.start_alarm()

        ## Write values to pcua
        try:
            opc.write_value('RedLED', 'Status', led_red)
            opc.write_value('OrangeLED', 'Status', led_orange)
            opc.write_value('GreenLED', 'Status', led_green)
            opc.write_value('Temperature', 'Value', temperature[0])
            opc.write_value('Humidity', 'Value', humidity[0])
            opc.write_value('AirPressure', 'Value', airpressure[0])
            opc.write_value('AirQuality', 'Value', airquality)
        except Exception as ex:
            print(f'Writing sensor_value to opcua_server error: {ex}')

        # Update LCD-Display
        lcd.change_screen_text('sensor1', (f'Temp: <value type="number" decimals="4">{temperature[0]}</value> C',
                                           f'Humi: <value type="number" decimals="4">{humidity[0]}</value> %'))
        lcd.change_screen_text('sensor2', (f'AirP: <value type="number" decimals="4">{airpressure[0]}</value> hPa',
                                                   f'AirQ: <value type="number" decimals="4">{airquality}</value> ppm'))

        time.sleep(10)

# Init Movement Sensor
def init_movement_sensor(opcua, movement_sensor):
    opc = opcua

    def update_movement_sensor(sender, args):
        try:
            opc.write_value('Presence', 'Value', args['new'])
            opc.write_value('Presence', 'Timestamp', time.time())
        except Exception as ex:
            print(f'Opcua Write Value: {ex}')
    movement_sensor.PresenceChanged.subscribe(update_movement_sensor)
    movement_sensor.start_measurement()

# Thread for status LED
def status_led_thread(args):
    connection_helper = ConnectionHelper(args['opc'])
    connection_helper.start_connection_check()
    led_stripe = args['led_stripe']

    while True:
        if connection_helper.Status == connection_helper.OK:
            led_stripe.BlueLED.Short_Blink(connection_helper.OK)
        if connection_helper.Status == connection_helper.OPCUA_SERVER_NOT_REACHABLE:
            led_stripe.BlueLED.Short_Blink(connection_helper.OPCUA_SERVER_NOT_REACHABLE)
        if connection_helper.Status == connection_helper.SERVER_NODE_NOT_REACHABLE:
            led_stripe.BlueLED.Short_Blink(connection_helper.SERVER_NODE_NOT_REACHABLE)
        if connection_helper.Status == connection_helper.VPN_GATEWAY_NOT_REACHABLE:
            led_stripe.BlueLED.Short_Blink(connection_helper.VPN_GATEWAY_NOT_REACHABLE)
        if connection_helper.Status == connection_helper.NO_INTERNET_CONNECTION:
            led_stripe.BlueLED.Short_Blink(connection_helper.NO_INTERNET_CONNECTION)

        time.sleep(10)

# Configurate Update for lcd display
def init_lcd_update(args):
    opcua_client = args['client']
    sys_info = args['sysinfo']

    lcd.add_screen('opcua'  , ('Das ist ein','OPCUA-Screen'))
    lcd.show_screen_name('opcua')
    lcd.set_backlight(True)
    lcd.start_update()

    ts = TemplateString(opcua_client)

    # Update text on opcua screen
    def update_opcua_screen(sender, args):
        if args['new'] == None:
            return

        # Get last element of node id
        line = str(args['node']).split('.')[-1]

        # Get current text for opcua screen and update the correct line
        text = lcd.get_screen('opcua')['Text']

        if line == 'TextLine1':
            text = (args['new'].ljust(16), text[1])
        elif line == 'TextLine2':
            text = (text[0], args['new'].ljust(16))
        lcd.change_screen_text('opcua', text)

    # Resolve value for templated string
    def resolve_templated_string(sender, args):
        text = (ts.resolve_template_string(args['screen']['Text'][0]),
                ts.resolve_template_string(args['screen']['Text'][1]))
        lcd.Text = text

    lcd.ResolveString.subscribe(resolve_templated_string)

    node1 = opcua_client.get_node(f'ns=2;s=SensorNode_{sys_info.Hostname[-1]}.Actuators.1602A.TextLine1')
    node2 = opcua_client.get_node(f'ns=2;s=SensorNode_{sys_info.Hostname[-1]}.Actuators.1602A.TextLine2')

    handler = OpcuaSubscriptionHandler()
    handler.DataChanged.subscribe(update_opcua_screen)

    sub = opcua_client.create_subscription(500, handler)
    sub.subscribe_data_change(node1)
    sub.subscribe_data_change(node2)

# setup mq135 calibration
def setup_mq135_calibration(sensors_actors_helpers):
    mq135 = sensors_actors_helpers['mq135']
    bme280 = sensors_actors_helpers['bme280']
    menu = sensors_actors_helpers['menu']
    movement_sensor = sensors_actors_helpers['movement']

    def start_calibration(sender, args):
        #movement_sensor.stop_measurement()
        mq135.start_calibration(args['ppm'], bme280.temperature[0], bme280.humidity[0])
        menu.Calibrated = mq135.Calibrated
        menu.CalibrationRunning = False
        #movement_sensor.start_measurement()

    menu.CalibrationStart.subscribe(start_calibration)

# Write systeminformation to opcua
def write_systeminformation_to_server(opc, sys_info):
    opc.write_value('HardwarePlatform'  , 'IP_Address'  , sys_info.IP)
    opc.write_value('Hardware'          , 'Architecture', sys_info.Architecture)
    opc.write_value('Hardware'          , 'ModelName'   , sys_info.ModelName)
    opc.write_value('Hardware'          , 'NumberOfCpus', sys_info.NumberOfCpus)
    opc.write_value('Hardware'          , 'Vendor'      , sys_info.Vendor)
    opc.write_value('OperatingSystem'   , 'Distributor' , sys_info.Distributor)
    opc.write_value('OperatingSystem'   , 'Release'     , sys_info.Release)
    opc.write_value('OperatingSystem'   , 'ReleaseName' , sys_info.ReleaseName)
    opc.write_value('OperatingSystem'   , 'Version'     , sys_info.Version)

import os
def wait_for_server(server_address):
    connected = False
    error_count = 0

    while not connected:
        time.sleep(10)
        response = os.system("ping -c 1 " + server_address)
        if response == 0:
            connected = True
        else:
            error_count += 1
            if error_count > 18:
                os.system("echo Connection Timeout > error.log")

if __name__ == "__main__":
    # Wait for RPi to be fully powered on
    wait_for_server(SERVER_ADDRESS)

    # Initialize I2C
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)

    # Initialize Sensors
    bme280 = BME280Sensor(0x77, bus)
    mq135 = MQ135(0, uc)
    movement_sensor = MovementSensor(17)

    # Initialize Actors
    lcd = LcdDisplay()
    led_stripe = LedStripe()
    piezo = Piezo(uc, 4)

    # Initialize helpers
    sys_info = SystemInformation()

    # Initialize OPCUA
    opcua_client = Client(f"opc.tcp://{SERVER_ADDRESS}:{OPCUA_PORT}")
    try:
        opcua_client.connect()   
    except Exception as ex:
        print(f'Opcua Client connect: {ex}')
        exit()
    opc = OpcuaHelper(opcua_client, sys_info.Hostname[-1])

    # Start menu
    music = MusicHelper(piezo)
    menu = Menu(lcd, music)

    # Dictionary for all sensors, actors and helpers
    sensors_actors_helpers = {
        'bme280'        : bme280,
        'mq135'         : mq135,
        'lcd'           : lcd,
        'led_stripe'    : led_stripe,
        'piezo'         : piezo,
        'client'        : opcua_client,
        'opc'           : opc,
        'sysinfo'       : sys_info,
        'movement'      : movement_sensor,
        'menu'          : menu
    }

    # Initialize sensornode --> call server and setup nodes
    initialize_sensornode(sys_info.Hostname[-1])

    # Write system information to opcua
    write_systeminformation_to_server(opc, sys_info)

    # Start threads
    t = Thread(target=measurement_thread, args=[sensors_actors_helpers])
    t.start()
    t2 = Thread(target=status_led_thread, args=[sensors_actors_helpers])
    t2.start()

    # Initialize everything for movement sensor
    init_movement_sensor(opc, movement_sensor)

    # Update for lcd display
    init_lcd_update(sensors_actors_helpers)

    # Setup MQ135 calibration
    setup_mq135_calibration(sensors_actors_helpers)

    # Show first lcd screen
    lcd.show_screen_index(0)
