from actors.actor_base import ActorBase
from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

class LcdDisplay(ActorBase):
    def __init__(self):
        self.__text = ('','')
        self.__display = {
            "BL" : 11,  # Backlight
            "EN" : 26,
            "RS" : 20,
            "D4" : 19,
            "D5" : 13,
            "D6" :  6,
            "D7" :  5,
        }
        self.__lcd = self.__get_lcd_display()
        self.__gpio_init()
        self.__screens = []
        self.__current_screen = ''

        self.__add_custom_characters()

    def __add_custom_characters(self):
        self.__lcd.create_char(0, (
            0b00000,    
            0b00001,    
            0b00011,    
            0b10110,    
            0b11100,    
            0b01000,    
            0b00000,   
            0b00000   
        ))

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__display["BL"], GPIO.OUT)

    def set_backlight(self, value):
        GPIO.output(self.__display["BL"], value)
    
    def __write_config(self):
        displayfunction = self.__lcd.data_bus_mode | 0x00
        displayfunction |= 0x08
        self.__lcd.command(0x20 | displayfunction)
        time.sleep(50e-6)
        self.__lcd.clear()

    def __write_text_to_display(self, text):
        #self.__lcd.close(clear=True)
        #self.__lcd = self.__get_lcd_display()
        self.__write_config()

        # Write first line
        self.__lcd.cursur_pos = (0, 0)
        self.__lcd.write_string(text[0][:16].ljust(16))

        # Write second line
        self.__lcd.cursor_pos = (1, 0)
        self.__lcd.write_string(text[1][:16].ljust(16))

        self.__text = text 

    def __get_lcd_display(self):
        lcd = None
        try:
            lcd = CharLCD(cols=16, rows=2, numbering_mode=GPIO.BCM, 
                          pin_rs=self.__display["RS"], pin_e=self.__display["EN"], 
                          pins_data=[self.__display[key] for key in ["D4", "D5", "D6", "D7"]])
        except:
            print('Getting lcd display failed')
        finally:
            return lcd

    def add_screen(self, name, text=('','')):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) > 0:
            print(f"Screen {name} is already there")
            return

        self.__screens.append({'Name' : name, 'Text' : text})

    def get_screen(self, name):
        screen = [screen['Name'] for screen in self.__screens if screen['Name'] == name]
        if len(screen) <= 0:
            print(f"Screen {name} does not exist")
        else: 
            return screen

    def remove_screen(self, name):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f'Screen {name} does not exist')

        # If Screen is currently shown, then show default screen
        if self.CurrentScreen == name:
            self.show_screen_index(0)

        # Remove screen from list
        self.__screens = [screen for screen in self.__screens if screen['Name'] != name]

    def show_screen_index(self, index):
        if index > len(self.__screens) - 1:
            print(f"Screen Index {index} does not exist")
            return

        self.text = self.__screens[index]['Text']

    def show_screen_name(self, name):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f"Screen with name {name} does not exist")
            return

        scr = [screen for screen in self.__screens if screen['Name'] == name][0]
        self.text = scr['Text']
        self.__current_screen = scr['Name']

    def change_screen_text(self, name, text):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f"Screen with name {name} does not exist")
            return

        next(s for s in self.__screens if s["Name"] == name)["Text"] = text

    # --- Display Text ----------------------------------------------------------
    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self, new_text):
        self.__text = new_text
        self.__write_text_to_display(new_text)
    # ---------------------------------------------------------------------------

    # --- Current Screen --------------------------------------------------------
    @property
    def CurrentScreen(self):
        return self.__current_screen
    @CurrentScreen.setter
    def CurrentScreen(self, screen):
        self.show_screen_name(screen)
    # ---------------------------------------------------------------------------

    # --- ScreenCount -----------------------------------------------------------
    @property
    def ScreenCount(self):
        return len(self.__screens)
    # ---------------------------------------------------------------------------

    def __del__(self):
        self.show_screen_index(0)
