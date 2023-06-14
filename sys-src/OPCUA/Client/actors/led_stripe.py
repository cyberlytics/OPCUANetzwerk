from actors.actor_base import ActorBase
from actors.led import Led
import RPi.GPIO as GPIO

class LedStripe(ActorBase):
    def __init__(self):
        self.__green_led  = Led(9)
        self.__orange_led = Led(8)
        self.__red_led    = Led(7)
        self.__blue_led   = Led(12)

    @property
    def GreenLED(self):
        return self.__green_led

    @property
    def OrangeLED(self):
        return self.__orange_led

    @property
    def RedLED(self):
        return self.__red_led

    @property
    def BlueLED(self):
        return self.__blue_led

    def red_on(self):
        self.RedLED.Status    = True
        self.OrangeLED.Status = False
        self.GreenLED.Status  = False

    def orange_on(self):
        self.RedLED.Status    = False
        self.OrangeLED.Status = True
        self.GreenLED.Status  = False

    def green_on(self):
        self.RedLED.Status    = False
        self.OrangeLED.Status = False
        self.GreenLED.Status  = True



