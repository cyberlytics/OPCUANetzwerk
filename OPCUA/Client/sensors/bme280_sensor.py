from sensors.bme280_temperature import BME280Temperature
from sensors.bme280_humidity import BME280Humidity
from sensors.bme280_airpressure import BME280AirPressure

import smbus2
import bme280
import time

class BME280Sensor():
    def __init__(self, I2CAddress, bus):
        self.__i2caddress = I2CAddress
        self.__calibration_params = None
        self.__bus = bus

        self.__temperature_sensor = BME280Temperature()
        self.__humidity_sensor = BME280Humidity()
        self.__airpressure_sensor = BME280AirPressure()
        self.__lastread_timestamp = 0

    # --- Temperature Sensor -----------------------------------------------------
    @property
    def temperature(self):
        self.read_sensor_values()
        return (self.__temperature_sensor.value, self.__temperature_sensor.unit, self.__temperature_sensor.timestamp)
    @temperature.setter
    def temperature(self, new_temperature):
        self.__temperature_sensor.value = new_temperature
    # ---------------------------------------------------------------------------

    # --- Humidty Sensor -----------------------------------------------------
    @property
    def humidity(self):
        self.read_sensor_values()
        return (self.__humidity_sensor.value, self.__humidity_sensor.unit, self.__humidity_sensor.timestamp)
    @humidity.setter
    def humidity(self, new_humidity):
        self.__humidity_sensor.value = new_humidity
    # ---------------------------------------------------------------------------

    # --- Air Pressure ----------------------------------------------------------
    @property
    def airpressure(self):
        self.read_sensor_values()
        return (self.__airpressure_sensor.value, self.__airpressure_sensor.unit, self.__airpressure_sensor.timestamp)
    @airpressure.setter
    def airpressure(self, new_airpressure):
        self.__airpressure_sensor.value = new_airpressure
    # ---------------------------------------------------------------------------

    def __read_calibration_params(self,i2cadress, bus):
        try:
            self.__calibration_params = bme280.load_calibration_params(bus, i2cadress)
        except:
            print("Loading of calibration params not successful")

    def read_sensor_values(self):
        # Only read new data every minute
        if time.time() - self.__lastread_timestamp < 60:
            return

        # If no calibration params are present, then read them
        if self.__calibration_params == None:
            self.__read_calibration_params(self.__i2caddress, self.__bus)

        # Try to read data
        try:
            if self.__calibration_params != None:
                data = bme280.sample(self.__bus, self.__i2caddress, self.__calibration_params)
            else:
                return
        except Exception as ex:
            print(f"Reading of values not successful: {ex}")
            return

        # Parse data into correct objects
        self.temperature = data.temperature
        self.__temperature_sensor.timestamp = time.time()

        self.humidity = data.humidity
        self.__humidity_sensor.timestamp = time.time()

        self.airpressure = data.pressure
        self.__airpressure_sensor.timestamp = time.time()

        # Write time of reading
        self.__lastread_timestamp = time.time()


