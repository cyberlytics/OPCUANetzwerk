from sensors.sensor_base import SensorBase
from libs.extension import Prescaler, RefVoltage
import time, math
import queue
import numpy as np

class MQ135(object):
    def __init__(self, gpio_pin, uc):
        super().__init__()

        # Initialize uc
        self.__uc = uc
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
        self.__ATMOCO2 = 417.0 # ppm nov 2022
        
        # class properties
        self.__rload = 5.1 # The load resistance on the board in kOhm
        self.__rzero = 48.3 # Calibration resistance at atmospheric CO2 level
        self.__calibrated = False
        self.__curently_calibrating = False
    
    # ----------------------------------------------------------
    # Properties -----------------------------------------------
    # ----------------------------------------------------------
    @property
    def CurrentlyCalibrating(self):
        return self.__curently_calibrating
    def __set_currently_calibrating(self, new_value):
        self.__curently_calibrating = new_value

    @property
    def Calibrated(self):
        return self.__calibrated
    def __set_calibrated(self, new_value):
        self.__calibrated = new_value
    # ----------------------------------------------------------
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    # Methods --------------------------------------------------
    # ----------------------------------------------------------

    def start_calibration(self, ppm, temperature, humidity, maxq=20, sampling_interval=1): 
        self.__ATMOCO2 == ppm
        self.__set_currently_calibrating(True)
        time_start = time.time()
        
        q = []
        rzero = None
        for i in range(maxq):
            try:
                rzero =  self.__get_corrected_resistance(temperature, humidity)
            except Exception as ex:
                print(f"Fehler beim Holen von R0: {ex}")
            
            q.append(rzero)
            time.sleep(sampling_interval)

        while np.std(q) > 0.1:
            print(np.std(q))
            q.pop(0)
            try:
                rzero =  self.__get_corrected_resistance(temperature, humidity)
            except Exception as ex:
                print(f"Fehler beim Holen von R0: {ex}")
            q.append(rzero)
            time.sleep(sampling_interval)

            # Timeout
            if time.time() - time_start > 120:
                self.__set_calibrated(False)
                self.__set_currently_calibrating(False)
                return False

        # return for success
        self.__rzero = np.mean(q)
        self.__set_calibrated(True)
        self.__set_currently_calibrating(False)
        return True

    def __get_correction_factor(self, temperature, humidity):
        if (temperature < 20):
            return self.__CORA * (temperature ** 2) - self.__CORB * temperature + self.__CORC - (humidity-33.) * self.__CORD
        else:
            return self.__CORE * temperature + self.__CORF * humidity + self.__CORG

    def __get_resistance(self):
        val = self.__uc.sample(self.__pin, Prescaler.P128, RefVoltage.V1_1)
        return (5. / 1.1 * 1023. / val - 1.) * self.__rload

    def __get_corrected_resistance(self, temperature, humidity):
        return self.__get_resistance() / self.__get_correction_factor(temperature, humidity)

    def get_ppm(self):
        return self.__PARA * ((self.__get_resistance() / self.__rzero) ** -self.__PARB)

    def get_corrected_ppm(self, temperature, humidity):
        return self.__PARA * ((self.__get_corrected_resistance(temperature, humidity) / self.__rzero) ** -self.__PARB)

    def __get_rzero(self):
        return self.__get_resistance() * ((self.__ATMOCO2 / self.__PARA) ** (1 / self.__PARB))
        
    def get_corrected_rzero(self, temperature, humidity):
        return self.__get_corrected_resistance(temperature, humidity) * ((self.__ATMOCO2 / self.__PARA) ** (1. / self.__PARB))

    # ----------------------------------------------------------
    # ----------------------------------------------------------

