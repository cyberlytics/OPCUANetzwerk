import music.shenanigans as shenanigans

from sensors.buttons import Buttons

from helpers.event_handler import EventHandler

import time
from threading import Thread

class Menu(object):
    
    def __init__(self, lcd_display, music):
        """Menu(): Menu handling for LCD-Display and 4 Buttons
        """
        self.__buttons = Buttons()
        self.__lcd = lcd_display
        self.__music = music
        self.__special_function_thread = Thread(target=self.__special_function, args=[])
        self.__special_function_thread.start()
        self.__eh = EventHandler()
        
        # Callbacks hinterlegen
        self.__buttons.Button1.start_measurement()
        self.__buttons.Button4.start_measurement()

        self.__buttons.Button4.ButtonDown.subscribe(self.__start_calibrate)
        self.__buttons.Button1.ButtonDown.subscribe(self.__switch_screens)

        self.__calibrate_start = False
        self.__current_screen_index = 0
        self.__current_ppm = 500
        self.__calibration_running = None
        self.__calibrated = False

    # ----------------------------------------------------------
    # Threads --------------------------------------------------
    # ----------------------------------------------------------
    def __special_function(self):
        """Thread function for playing music when button 2 are button 3 are held down
        """
        while True:
            time.sleep(2.5)
            if self.__buttons.Button2.Status and self.__buttons.Button3.Status:
                start = time.time()
            while self.__buttons.Button2.Status and self.__buttons.Button3.Status:
                if time.time() - start > 5:
                    pass
                    self.__music.play(shenanigans.shenanigans)
    # ----------------------------------------------------------
    # ----------------------------------------------------------

    # ----------------------------------------------------------
    # Events ---------------------------------------------------
    # ----------------------------------------------------------
    def __switch_screens(self, sender, args):
        """ Switches curren shown lcd-screen to next
        """
        # Switch to next screen
        if self.__lcd.ScreenCount == 0:
            return False

        self.__current_screen_index = (self.__current_screen_index + 1) % (self.__lcd.ScreenCount)
        self.__lcd.show_screen_index(self.__current_screen_index)
        return True

    def __start_calibrate(self, sender, args):
        """Starts calibration for MQ135 Sensor if called two-times
        """

        # Other behavior when called second time
        if self.__calibrate_start:
            self.__start_mq135_calibration()
            self.__lcd.remove_screen('calibrate')
            self.__lcd.start_update()

            # Reset everything, so that calibration can be accessed again
            self.__calibrate_start = False
            return

        # Behavior for first call
        self.__lcd.add_screen('calibrate' , (f'    {self.__current_ppm} ppm',f' x   +    -   {chr(0x00)}'))
        self.__lcd.stop_update()
        self.__set_events_for_calibration()

        self.__lcd.show_screen_name('calibrate')

        self.__calibrate_start = True

    def __raise_ppm(self, sender, args):
        """Raises current shown ppm by 10
        """
        self.__current_ppm = self.__get_current_ppm() + 10
        self.__lcd.Text = (f'    {self.__current_ppm} ppm', self.__lcd.Text[1])

    def __lower_ppm(self, sender, args):
        """Lowers current shown ppm by 10
        """
        self.__current_ppm = self.__get_current_ppm() - 10
        self.__lcd.Text = (f'    {self.__current_ppm} ppm', self.__lcd.Text[1])

    def __abort_calibrate(self, sender, args):
        """Abort calibration and set menu functionality back to screen-switching
        """
        self.__lcd.remove_screen('calibrate')

        # Set Events for screen switching
        self.__unsubscribe_calibration_events()
        self.__set_events_for_screenswitch()

        self.__calibrate_start = False
        self.__lcd.show_screen_index(0)

    # ----------------------------------------------------------
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    # Helpers --------------------------------------------------
    # ----------------------------------------------------------
    def __get_current_ppm(self):
        """Extract current ppm from current shown text
        """
        old_text = self.__lcd.Text
        
        # Get current ppm from string
        return int(old_text[0].lstrip().split(' ')[0])

    def __unsubscribe_calibration_events(self):
        """Unsubscribe the events needed for calibration selection
        """
        self.__buttons.Button1.ButtonDown.unsubscribe(self.__abort_calibrate)
        self.__buttons.Button2.ButtonDown.unsubscribe(self.__raise_ppm)
        self.__buttons.Button3.ButtonDown.unsubscribe(self.__lower_ppm)
        self.__buttons.Button4.ButtonDown.unsubscribe(self.__start_calibrate)

    def __set_events_for_calibration(self):
        """Set Events for calibration selection
        """
        # Switch Events for Button 1
        self.__buttons.Button1.ButtonDown.unsubscribe(self.__switch_screens)
        self.__buttons.Button1.ButtonDown.subscribe(self.__abort_calibrate)

        # Activate measurement and events for button 2 and button 3 --> raise and lower ppm
        self.__buttons.Button2.start_measurement()
        self.__buttons.Button3.start_measurement()
        self.__buttons.Button2.ButtonDown.subscribe(self.__raise_ppm)
        self.__buttons.Button3.ButtonDown.subscribe(self.__lower_ppm)

    def __set_events_for_screenswitch(self):
        """Set Events for Screen-Switching
        """
        # Switch Events for Button 1 and Button 4
        self.__buttons.Button1.ButtonDown.subscribe(self.__switch_screens)
        self.__buttons.Button4.ButtonDown.subscribe(self.__start_calibrate)
    # ----------------------------------------------------------
    # ----------------------------------------------------------


    # ----------------------------------------------------------
    # Methods --------------------------------------------------
    # ----------------------------------------------------------
    def __start_mq135_calibration(self):
        """Starts calibration for MQ135 sensor when called
        -> Also shows calibration screen, while running

        After finishing calibration functionality gets set back to screenswitch
        """

        # Show screen for calibration
        t = Thread(target=self.__show_calibrating_screen, args=[])
        t.start()

        # Unsubscribe calibration events while running
        self.__unsubscribe_calibration_events()
        
        # Call event to inform Main Skript
        self.CalibrationRunning = True
        self.__eh(self, {'ppm' : self.__get_current_ppm()})

        # Set Events back to screen switching after finishing
        self.__set_events_for_screenswitch()

    def __show_calibrating_screen(self):
        """Show screen for calibrating mq135 sensor
        """
        time.sleep(1)

        self.__lcd.add_screen('calibrating1', ('MQ135 Sensor:','Calibrating.'))
        self.__lcd.add_screen('calibrating2', ('MQ135 Sensor:','Calibrating..'))
        self.__lcd.add_screen('calibrating3', ('MQ135 Sensor:','Calibrating...'))

        while self.CalibrationRunning:
            self.__lcd.show_screen_name('calibrating1')
            time.sleep(0.5)
            self.__lcd.show_screen_name('calibrating2')
            time.sleep(0.5)
            self.__lcd.show_screen_name('calibrating3')
            time.sleep(0.5)

        if self.Calibrated:
            self.__lcd.add_screen('calibration_finished', ('Calibration', 'was successful'))
        elif not self.Calibrated:
            self.__lcd.add_screen('calibration_finished', ('Calibration', 'has failed'))
        
        self.__lcd.show_screen_name('calibration_finished')
        time.sleep(3)
        self.__lcd.remove_screen('calibration_finished')
        self.__lcd.remove_screen('calibrating1')
        self.__lcd.remove_screen('calibrating2')
        self.__lcd.remove_screen('calibrating3')
    # ----------------------------------------------------------
    # ----------------------------------------------------------

    @property
    def CalibrationStart(self):
        return self.__eh

    @property
    def CalibrationRunning(self):
        return self.__calibration_running
    @CalibrationRunning.setter
    def CalibrationRunning(self, new_value):
        self.__calibration_running = new_value

    @property
    def Calibrated(self):
        return self.__calibrated
    @Calibrated.setter
    def Calibrated(self, new_value):
        self.__calibrated = new_value