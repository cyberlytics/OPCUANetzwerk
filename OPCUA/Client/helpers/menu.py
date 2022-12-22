from sensors.buttons import Buttons
from sensors.bme280_sensor import BME280Sensor
from sensors.mq135 import MQ135
from actors.lcd_display import LcdDisplay
import helpers.globals as globals

import time
from threading import Thread

class Menu(object):
    def __init__(self):
        self.__buttons = Buttons()
        
        # Callbacks hinterlegen
        self.__buttons.Button1.start_measurement()
        self.__buttons.Button4.start_measurement()

        self.__buttons.Button4.ButtonDown.subscribe(self.__start_calibrate)
        self.__buttons.Button1.ButtonDown.subscribe(self.__switch_screens)

        self.__calibrate_start = False
        self.__current_screen_index = 0
        self.__current_ppm = 500

        globals.lcd.add_screen('calibrate' , (f'    {self.__current_ppm} ppm',f' x   +    -   {chr(0x00)}'))

    # ----------------------------------------------------------
    # Events ---------------------------------------------------
    # ----------------------------------------------------------
    def __switch_screens(self, sender, args):
        # Switch to next screen
        self.__current_screen_index = (self.__current_screen_index + 1) % (globals.lcd.ScreenCount - 1)
        globals.lcd.show_screen_index(self.__current_screen_index)

    def __start_calibrate(self, sender, args):
        if self.__calibrate_start:
            self.__unsubscribe_calibration_events()
            self.__calibrate_start = False
            self.__start_mq135_calibration()
            self.__set_events_for_screenswitch()
            return

        self.__set_events_for_calibration()

        globals.lcd.show_screen_name('calibrate')

        self.__calibrate_start = True

    def __raise_ppm(self, sender, args):
        self.__current_ppm = self.__get_current_ppm() + 10
        globals.lcd.text = (f'    {self.__current_ppm} ppm', globals.lcd.text[1])

    def __lower_ppm(self, sender, args):
        self.__current_ppm = self.__get_current_ppm() - 10
        globals.lcd.text = (f'    {self.__current_ppm} ppm', globals.lcd.text[1])

    def __abort_calibrate(self, sender, args):
        # Set Events for screen switching
        self.__set_events_for_screenswitch()

        self.__calibrate_start = False
        globals.lcd.show_screen_index(0)

    # ----------------------------------------------------------
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    # Helpers --------------------------------------------------
    # ----------------------------------------------------------
    def __get_current_ppm(self):
        old_text = globals.lcd.text
        
        # Get current ppm from string
        return int(old_text[0].lstrip().split(' ')[0])

    def __unsubscribe_calibration_events(self):
        self.__buttons.Button1.ButtonDown.unsubscribe(self.__abort_calibrate)
        self.__buttons.Button2.ButtonDown.unsubscribe(self.__raise_ppm)
        self.__buttons.Button3.ButtonDown.unsubscribe(self.__lower_ppm)
        self.__buttons.Button4.ButtonDown.unsubscribe(self.__start_calibrate)

        self.__buttons.Button2.stop_measurement()
        self.__buttons.Button3.stop_measurement()

    def __set_events_for_calibration(self):
        # Switch Events for Button 1
        self.__buttons.Button1.ButtonDown.unsubscribe(self.__switch_screens)
        self.__buttons.Button1.ButtonDown.subscribe(self.__abort_calibrate)

        # Activate measurement and events for button 2 and button 3 --> raise and lower ppm
        self.__buttons.Button2.start_measurement()
        self.__buttons.Button3.start_measurement()
        self.__buttons.Button2.ButtonDown.subscribe(self.__raise_ppm)
        self.__buttons.Button3.ButtonDown.subscribe(self.__lower_ppm)

    def __set_events_for_screenswitch(self):
        # Switch Events for Button 1
        self.__buttons.Button1.ButtonDown.subscribe(self.__switch_screens)
        self.__buttons.Button4.ButtonDown.subscribe(self.__start_calibrate)
    # ----------------------------------------------------------
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    # Methods --------------------------------------------------
    # ----------------------------------------------------------
    def __start_mq135_calibration(self):
        t = Thread(target=self.__show_calibrating_screen, args=[])
        t.start()
        globals.mq135.start_calibration(self.__current_ppm, globals.bme280.temperature[0], globals.bme280.humidity[0])

    def __show_calibrating_screen(self):
        time.sleep(1)

        globals.lcd.add_screen('calibrating1', ('MQ135 Sensor:','Calibrating.'))
        globals.lcd.add_screen('calibrating2', ('MQ135 Sensor:','Calibrating..'))
        globals.lcd.add_screen('calibrating3', ('MQ135 Sensor:','Calibrating...'))

        while globals.mq135.CurrentlyCalibrating:
            globals.lcd.show_screen_name('calibrating1')
            time.sleep(0.5)
            globals.lcd.show_screen_name('calibrating2')
            time.sleep(0.5)
            globals.lcd.show_screen_name('calibrating3')
            time.sleep(0.5)

        if globals.mq135.Calibrated:
            globals.lcd.add_screen('calibration_finished', ('Calibration', 'was successful'))
        elif not globals.mq135.Calibrated:
            globals.lcd.add_screen('calibration_finished', ('Calibration', 'has failed'))
        
        globals.lcd.show_screen_name('calibration_finished')
        time.sleep(3)
        globals.lcd.remove_screen('calibration_finished')
        globals.lcd.remove_screen('calibrating1')
        globals.lcd.remove_screen('calibrating2')
        globals.lcd.remove_screen('calibrating3')
    # ----------------------------------------------------------
    # ----------------------------------------------------------
