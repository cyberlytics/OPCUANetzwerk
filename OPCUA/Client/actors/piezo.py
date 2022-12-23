from actors.actor_base import ActorBase

from libs.extension import Microcontroller, UCException, Prescaler, RefVoltage

import time
from threading import Thread


class Piezo(ActorBase):
    def __init__(self, uc):
        self.__max_duration = 5 * 1000000 # In MicroSeconds
        self.__alarm_active = False
        self.__uc = uc
        self.__frequency = 440


    def play_tone(self, frequency, duration=None):
        dur = duration
        if dur != None:
            if (dur * 1000000 > self.__max_duration):
                dur = self.__max_duration

        if duration == None:
            self.__uc.playFrequency(4, frequency)
        else:
            self.__uc.playFrequency(4, frequency, dur)

    def __alarm(self):
        while(self.__alarm_active):
            self.__play(3000000, self.Frequency)
            time.sleep(.5)

    def start_alarm(self):
        if self.__alarm_active:
            return
        self.__alarm_active = True
        self.__t = Thread(target=self.__alarm, args=[])
        self.__t.start()

    def stop_alarm(self):
        self.__alarm_active = False

    # --- Frequency -------------------------------------------------------------
    @property
    def Frequency(self):
        return self.__frequency
    @Frequency.setter
    def Frequency(self, new_frequency):
        self.__frequency = new_frequency
    # ---------------------------------------------------------------------------




