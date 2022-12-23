from actors.actor_base import ActorBase
import RPi.GPIO as GPIO
import time

class Led(object):
    def __init__(self, pin):
        self.__pin = pin
        self.__gpio_init()

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)

    # --- Status ----------------------------------------------------------------
    @property
    def Status(self):
        return self.__status
    @Status.setter
    def Status(self, new_status):
        self.__status = new_status
        self.__set_status(self.__status)
    # ---------------------------------------------------------------------------

    def __set_status(self, status):
        GPIO.output(self.__pin, status)

    def Short_Blink(self, blink_times):
        for i in range(blink_times):
            self.Status = True
            time.sleep(0.2)
            self.Status = False
            time.sleep(0.2)
        

    def __toggle(self):
        self.status = not self.status