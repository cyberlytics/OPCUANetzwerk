from actors.piezo import Piezo
from libs.extension import Microcontroller, RefVoltage, Prescaler

from helpers.systeminformation import SystemInformation
from helpers.opcua_helper import OpcuaHelper
from helpers.connection_helper import ConnectionHelper

from sensors.buttons import Buttons
from sensors.bme280_sensor import BME280Sensor
from sensors.mq135 import MQ135
from sensors.movement_sensor import MovementSensor

from opcua import Client
import smbus2

from actors.lcd_display import LcdDisplay
from actors.led_stripe import LedStripe
from actors.piezo import Piezo

import time

# CONSTANTS ---------------------------------
SERVER_ADDRESS         = 'server.sn.local'
OPCUA_PORT             = 4841
# -------------------------------------------

# GLOBAL VARIABLES --------------------------
# -------------------------------------------

def init():
    # Initialize I2C
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)

    # Initialize Sensors
    global bme280
    bme280 = BME280Sensor(0x77, bus)
    global mq135
    mq135 = MQ135(0, uc)
    global movement_sensor
    movement_sensor = MovementSensor(17)

    # Initialize Actors
    global lcd
    lcd = LcdDisplay()
    global led_stripe
    led_stripe = LedStripe()
    global piezo
    piezo = Piezo(uc)

    # Initialize Helpers
    global sys_info
    sys_info = SystemInformation()

    # Initialize OPCUA
    global opcua_client
    opcua_client = Client(f"opc.tcp://{SERVER_ADDRESS}:{OPCUA_PORT}")
    try:
        opcua_client.connect()   
    except Exception as ex:
        print(f'Opcua Client connect: {ex}')
        exit()

    global opc
    opc = OpcuaHelper(opcua_client, sys_info.hostname[-1])

    # Initialize Connection Check
    global connection_helper
    connection_helper = ConnectionHelper()
    connection_helper.start_connection_check()

class AirQuality():
    WarningLevel = 800
    AlarmLevel = 1200