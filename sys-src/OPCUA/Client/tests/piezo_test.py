import sys
sys.path.insert(0, '..')

from actors.piezo import Piezo
from libs.extension import Microcontroller, RefVoltage, Prescaler
import smbus2, time

def test_piezo_alarm():
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)
    uc.enable(True)

    piezo = Piezo(uc, 4)
    result = piezo.start_alarm()
    assert result == True
    print('Now a alarm should be heard for 20 seconds')
    time.sleep(20)
    piezo.stop_alarm()

    piezo.Frequency = 880
    result = piezo.start_alarm()
    assert result == True
    print('Now a alarm with higher tone should be heard for 20 seconds')
    time.sleep(20)
    piezo.stop_alarm()
    uc.enable(False)

def test_piezo_double_start():
    bus = smbus2.SMBus(1)
    rst_pin = 10
    add = 100
    uc = Microcontroller(bus, rst_pin, add)
    uc.enable(True)

    piezo = Piezo(uc, 4)
    result = piezo.start_alarm()
    assert result == True
    result = piezo.start_alarm()
    assert result == False
    piezo.stop_alarm()
    time.sleep(1)

    uc.enable(False)