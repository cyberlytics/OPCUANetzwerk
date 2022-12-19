from actors.actor_base import ActorBase
from actors.led import Led
import RPi.GPIO as GPIO

class LedStripe(ActorBase):
    def __init__(self):
        self.__green_led  = Led(9)
        self.__orange_led = Led(8)
        self.__red_led    = Led(7)
        self.__blue_led   = Led(12)



