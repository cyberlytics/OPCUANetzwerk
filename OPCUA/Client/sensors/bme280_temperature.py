from sensors.sensor_base import SensorBase

class BME280Temperature(SensorBase):
    def __init__(self):
        super().__init__()