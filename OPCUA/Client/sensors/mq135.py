from sensors.sensor_base import SensorBase
from libs.extension import Microcontroller, RefVoltage, Prescaler
import smbus2

class MQ135(object):
    def __init__(self, gpio_pin):
        super().__init__()

        # Initialize uc
        bus = smbus2.SMBus(1)
        rst_pin = 10
        add = 100
        self.__uc = Microcontroller(bus, rst_pin, add)
        self.__uc.enable(True)

        # ADC values
        self.__pin = gpio_pin

        # Constants
        self.__PARA = 116.6020682
        self.__PARB = 2.769034857
        self.__CORA = .00035
        self.__CORB = .02718
        self.__CORC = 1.39538
        self.__CORD = .0018
        self.__CORE = -.003333333
        self.__CORF = -.001923077
        self.__CORG = 1.130128205
        self.__ATMOCO2 = 417.31 # ppm nov 2022
        
        # class properties
        self.__rload = 1.0 # The load resistance on the board in kOhm
        self.__rzero = None # Calibration resistance at atmospheric CO2 level
        self.__rzero = self.__get_resistance()
    
    def set_corrected_rzero(self, temperature, humidity):
        self.__rzero = self.__get_corrected_resistance(temperature, humidity)

    def __get_correction_factor(self, temperature, humidity):
        if (temperature < 20):
            return self.__CORA * (temperature ** 2) - self.__CORB * temperature + self.__CORC - (humidity-33.) * self.__CORD
        else:
            return self.__CORE * temperature + self.__CORF * humidity + self.__CORG

    def __get_resistance(self):
        val = self.__uc.sample(self.__pin, Prescaler.P128, RefVoltage.V1_1)
        return ((1023. / val) - 1.) * self.__rload

    def __get_corrected_resistance(self, temperature, humidity):
        return self.__get_resistance() / self.__get_correction_factor(temperature, humidity)

    def __get_ppm(self):
        return self.__PARA * ((self.__get_resistance() / self.__rzero) ** -self.__PARB)

    def get_corrected_ppm(self, temperature, humidity):
        return self.__PARA * ((self.__get_corrected_resistance(temperature, humidity) / self.__rzero) ** -self.__PARB)

    def __get_rzero(self):
        return self.__get_resistance() * ((self.__ATMOCO2 / self.__PARA) ** (1 / self.__PARB))
        
    def __get_corrected_rzero(self, temperature, humidity):
        return self.__get_corrected_resistance(temperature, humidity) * ((self.__ATMOCO2 / self.__PARA) ** (1. / self.__PARB))




