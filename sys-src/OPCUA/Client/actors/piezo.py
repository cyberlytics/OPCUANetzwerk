from actors.actor_base import ActorBase

from libs.extension import Microcontroller, UCException, Prescaler, RefVoltage

import time
from threading import Thread


class Piezo(ActorBase):
    def __init__(self, uc, pin):
        self.__max_duration = 5 * 1000000 # In MicroSeconds
        self.__alarm_active = False
        self.__uc = uc
        self.__pin = pin
        self.__frequency = 440

        # Alarm configuration
        self.__alarm_freq = 440
        self.__alarm_on_dur = .2
        self.__alarm_off_dur = 5

    def __play_tone(self, frequency, duration=None):
        dur = duration
        if dur != None:
            if (dur * 1000000 > self.__max_duration):
                dur = self.__max_duration

        if duration == None:
            self.__uc.playFrequency(self.__pin, frequency)
        else:
            self.__uc.playFrequency(self.__pin, frequency, dur)

    def playFrequency(self, frequency, dur):
        self.__uc.playFrequency(self.__pin, frequency, dur)

    def __alarm(self):
        while(self.__alarm_active):
            self.__play_tone(self.__alarm_freq)
            time.sleep(self.__alarm_on_dur)
            self.__play_tone(0)
            time.sleep(self.__alarm_off_dur)

    def start_alarm(self):
        if self.__alarm_active:
            return False
        self.__alarm_active = True
        self.__t = Thread(target=self.__alarm, args=[])
        self.__t.start()
        return True

    def stop_alarm(self):
        self.__alarm_active = False

    # --- Frequency -------------------------------------------------------------
    @property
    def Frequency(self):
        return self.__alarm_freq
    @Frequency.setter
    def Frequency(self, new_frequency):
        self.__alarm_freq = new_frequency
    # ---------------------------------------------------------------------------




