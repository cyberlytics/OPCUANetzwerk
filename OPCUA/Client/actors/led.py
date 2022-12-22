from actors.actor_base import ActorBase
import RPi.GPIO as GPIO

class Led(object):
    def __init__(self, pin):
        self.__pin = pin
        self.__gpio_init()

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)

    # --- Status ----------------------------------------------------------------
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, new_status):
        self.__status = new_status
        self.__set_status(self.__status)
    # ---------------------------------------------------------------------------

    def __set_status(self, status):
        GPIO.output(self.__pin, status)

    def __toggle(self):
        self.status = not self.status