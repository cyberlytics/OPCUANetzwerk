from sensors.sensor_base import SensorBase
from helpers.event_handler import EventHandler

import RPi.GPIO as GPIO
from threading import Thread
import time

class MovementSensor(SensorBase):
    def __init__(self, pin):
        super().__init__()

        self.__pin = pin
        self.__presence = False
        self.__measuring_active = False

        self.__eh = EventHandler()

        self.__gpio_init()

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.IN)

    def __measure(self):
        last_movement_time = 0

        while(self.__measuring_active):
            movement = GPIO.input(self.__pin)

            # Movement --> Reset timer
            if movement:
                last_movement_time = time.time()

            # Pin is high and no presence -> presence starts
            if not self.Presence and movement:
                self.__set_presence(True)

            # No movement for a minute --> Presence ends
            if self.__presence and not movement and time.time() - last_movement_time > 60:
                self.__set_presence(False)

            time.sleep(.2)

    def start_measurement(self):
        if self.__measuring_active:
            return False

        self.__measuring_active = True
        self.__t = Thread(target=self.__measure, args=[])
        self.__t.start()
        return True

    def stop_measurement(self):
        self.__measuring_active = False
        self.__presence = False


    # --- Presence --------------------------------------------------------------
    @property
    def Presence(self):
        return self.__presence

    def __set_presence(self, value):
        self.__eh(self, {"old" : self.__presence, "new" : value})
        self.__presence = value
    # ---------------------------------------------------------------------------

    @property
    def PresenceChanged(self):
        return self.__eh
