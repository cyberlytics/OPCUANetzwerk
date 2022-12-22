from sensors.buttons import Buttons
from sensors.bme280_sensor import BME280Sensor
from sensors.mq135 import MQ135
from sensors.movement_sensor import MovementSensor

from actors.lcd_display import LcdDisplay
import time


def init():
    # Initialize Sensors
    global bme280
    bme280 = BME280Sensor(0x77)
    global mq135
    mq135 = MQ135(0)
    global movement_sensor
    movement_sensor = MovementSensor(17)

    # Initialize Actors
    global lcd
    lcd = LcdDisplay()

    # Initialize Helpers

    # Initialize OPCUA


