from actors.actor_base import ActorBase
import time
from threading import Thread

class LcdDisplay(ActorBase):
    def __init__(self):
        self.__max_duration = 1 # In Seconds
        self.__alarm_active = False
        self.__t = Thread(target=self.__alarm, args=[])

    def __play(self, duration, frequency):
        dur = duration
        if (dur > self.__max_duration):
            dur = self.__max_duration

        # ToDo:
        # Ansteuerung piezo

    def __alarm(self):
        while(self.__alarm_active):
            self.__play(.5, self.frequency)
            time.sleep(.5)

    def start_alarm(self):
        if self.__alarm_active:
            return
        self.__alarm_active = True
        self.__t.start()

    def stop_alarm(self):
        self.__alarm_active = False

    # --- Frequency -------------------------------------------------------------
    @property
    def frequency(self):
        return self.__frequency
    frequency.setter
    def temperature(self, new_frequency):
        self.__frequency = new_frequency
    # ---------------------------------------------------------------------------




