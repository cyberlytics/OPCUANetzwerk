from actors.actor_base import ActorBase
from RPLCD import CharLCD
import RPi.GPIO as GPIO

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

    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__display["BL"], GPIO.OUT)

    def set_backlight(self, value):
        GPIO.output(self.__display["BL"], value)
    
    def __write_text_to_display(self, text):
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

    # --- Display Text ----------------------------------------------------------
    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self, new_text):
        self.__text = new_text
        self.__write_text_to_display(new_text)
    # ---------------------------------------------------------------------------