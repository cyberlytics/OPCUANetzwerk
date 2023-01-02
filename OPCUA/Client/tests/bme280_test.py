import sys
sys.path.insert(0, '..')

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from sensors.bme280_sensor import BME280Sensor
from libs.extension import Microcontroller, RefVoltage, Prescaler
import smbus2, time, sys, socket, json


# Initialize I2C
def test_read_values_bme280():
    bus = smbus2.SMBus(1)
    bme280 = BME280Sensor(0x77, bus)
    print('Read values of bme280')

    t = bme280.temperature[0]
    h = bme280.humidity[0]
    a = bme280.airpressure[0]

    assert t != None
    assert h != None
    assert a != None

    print('Read values again after 3 seconds. Values should not change')
    time.sleep(3)

    # Test that values haven't changed
    
    tn = bme280.temperature[0]
    hn = bme280.humidity[0]
    an = bme280.airpressure[0]

    assert t == tn
    assert h == hn
    assert a == an

def test_read_new_values_bme280():
    bus = smbus2.SMBus(1)
    bme280 = BME280Sensor(0x77, bus)
    print('Read values of bme280')

    t = bme280.temperature[2]
    h = bme280.humidity[2]
    a = bme280.airpressure[2]

    assert t != None
    assert h != None
    assert a != None

    print('Read values again after 15 seconds. New read should occur')
    time.sleep(15)

    # Test that values haven't changed
    
    tn = bme280.temperature[2]
    hn = bme280.humidity[2]
    an = bme280.airpressure[2]

    assert t != tn
    assert h != hn
    assert a != an

def test_bme280_i2c():
    bus = smbus2.SMBus(1)
    bme280 = BME280Sensor(0x12, bus)

    assert bme280.read_sensor_values() == False