from sensors.mq135 import MQ135
from libs.extension import Microcontroller, RefVoltage, Prescaler
import smbus2

def test_mq135_read():
    # Initialize I2C
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)

    mq135 = MQ135(0, uc)

    assert mq135.get_ppm() != None

def test_mq135_corrected_read():
    # Initialize I2C
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)

    mq135 = MQ135(0, uc)

    # Test with example temperature
    assert mq135.get_corrected_ppm(20.0, 40.0) != None
