from sensors.mq135 import MQ135
from sensors.bme280_sensor import BME280Sensor

import time

bme280 = BME280Sensor(0x77)
mq135 = MQ135(0)
t = bme280.temperature[0]
h = bme280.humidity[0]


for i in range(10000):
    adc = mq135.get_adc_val()
    v = 1.1/1023. * adc

    t = bme280.temperature[0]
    h = bme280.humidity[0]
    #mq135.set_corrected_rzero(t, h)
    #ppm = mq135.get_corrected_ppm(bme280.temperature[0], bme280.humidity[0])

    print(f"Temperatur: {t}")
    print(f"Luftfeucht: {h}")
    print(f"R_Zero:     {mq135.get_corrected_rzero(t,h)}")
    print(f"ppm:        {mq135.get_corrected_ppm(t,h)}")
    print(f"ppm:        {mq135.get_ppm()}")
    print(f"ADC:        {v}")
    time.sleep(2)