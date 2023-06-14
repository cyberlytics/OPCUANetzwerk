from abc import ABC, abstractmethod

class SensorBase(ABC):
    def __init__(self):
        self.__value = None
        self.__unit = None
        self.__timestamp = None

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, new_value):
        self.__value = new_value

    @property
    def unit(self):
        return self.__unit
    @unit.setter
    def unit(self, new_unit):
        self.__unit = new_unit

    @property
    def timestamp(self):
        return self.__timestamp
    @timestamp.setter
    def timestamp(self, new_timestamp):
        self.__timestamp = new_timestamp