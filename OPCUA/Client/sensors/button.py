from os import pread
from sensors.sensor_base import SensorBase
import RPi.GPIO as GPIO
from threading import Thread
from helpers.event_handler import EventHandler
import time

class Button(SensorBase):
    def __init__(self, pin):
        self.__pin = pin
        self.__gpio_init()
        self.__measuring_active = False
        self.__eh_ButtonDown = EventHandler()
        self.__eh_ButtonStay = EventHandler()
        self.__eh_ButtonUp = EventHandler()

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.IN)


    def __measure(self):
        pressed_old = False
        while(self.__measuring_active):
            pressed = not GPIO.input(self.__pin)

            # Rising flank --> Button Down
            if not pressed_old and pressed:
                self.__eh_ButtonDown(self,None)

            # Current high --> Button hold
            if pressed_old and pressed:
                self.__eh_ButtonStay(self,None)

            # Falling Flank --> Button Up
            if pressed_old and not pressed:
                self.__eh_ButtonUp(self,None)

            pressed_old = pressed
            self.__set_status(pressed)
            time.sleep(0.1)

    def start_measurement(self):
        if self.__measuring_active:
            return

        self.__measuring_active = True
        self.__t = Thread(target=self.__measure, args=[])
        self.__t.start()

    def stop_measurement(self):
        self.__measuring_active = False

    # --- Status ----------------------------------------------------------------
    @property
    def status(self):
        return GPIO.input(self.__pin)

    def __set_status(self, value):
        self.__status = value
    # ---------------------------------------------------------------------------

    # --- ButtonEvents ------------------------------------------------------------
    @property
    def ButtonDown(self):
        return self.__eh_ButtonDown

    @property
    def ButtonUp(self):
        return self.__eh_ButtonUp

    @property
    def ButtonStay(self):
        return self.__eh_ButtonStay
    # -----------------------------------------------------------------------------



