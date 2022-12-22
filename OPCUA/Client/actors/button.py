from actors.actor_base import ActorBase
import RPi.GPIO as GPIO

class Button(ActorBase):
    def __init__(self, pin):
        self.__pin = pin

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.IN)

    # --- Status ----------------------------------------------------------------
    @property
    def status(self):
        return GPIO.input(self.__pin)

    def __set_status(self, value):
        self.__status = value
    # ---------------------------------------------------------------------------


