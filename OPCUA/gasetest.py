from sensors.mq135 import MQ135
from sensors.bme280_sensor import BME280Sensor

import time

bme280 = BME280Sensor(0x77)
mq135 = MQ135(0)

for i in range(1000):
    ppm = mq135.get_corrected_ppm(bme280.temperature, bme280.humidity)
    print(ppm)