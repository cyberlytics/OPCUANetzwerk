from tkinter import Text
from actors.actor_base import ActorBase

from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

class LcdDisplay(ActorBase):
    def __init__(self, client=None):
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

        self.__client = client

    # ----------------------------------------------------------
    # Hardware Functionality -----------------------------------
    # ----------------------------------------------------------
    
    # __add_custom_character()
    def __add_custom_characters(self):
        # Checkmark
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

    # __gpio_init()
    def __gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__display["BL"], GPIO.OUT)

    # set_backlight()
    def set_backlight(self, value):
        GPIO.output(self.__display["BL"], value)
    
    # write_config()
    def __write_config(self):
        displayfunction = self.__lcd.data_bus_mode | 0x00
        displayfunction |= 0x08
        self.__lcd.command(0x20 | displayfunction)
        time.sleep(50e-6)
        self.__lcd.clear()

    # __write_text_to_display()
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

    # __get_lcd_display()
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

    # ----------------------------------------------------------
    # ----------------------------------------------------------



    # ----------------------------------------------------------
    # Screen Functionality -------------------------------------
    # ----------------------------------------------------------

    # add_screen()
    def add_screen(self, name, text=('','')):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) > 0:
            print(f"Screen {name} is already there")
            return

        self.__screens.append({'Name' : name, 'Text' : text})

    # get_screen()
    def get_screen(self, name):
        screen = [screen for screen in self.__screens if screen['Name'] == name][0]
        if len(screen) <= 0:
            print(f"Screen {name} does not exist")
        else: 
            return screen

    # remove_screen()
    def remove_screen(self, name):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f'Screen {name} does not exist')

        # If Screen is currently shown, then show default screen
        if self.CurrentScreen == name:
            self.show_screen_index(0)

        # Remove screen from list
        self.__screens = [screen for screen in self.__screens if screen['Name'] != name]

    # show_screen_index()
    def show_screen_index(self, index):
        if index > len(self.__screens) - 1:
            print(f"Screen Index {index} does not exist")
            return

        text = (TemplateString.resolve_template_string(self.__screens[index]['Text'][0], self.__client),TemplateString.resolve_template_string(self.__screens[index]['Text'][1], self.__client))
        self.Text = text

        # Set current screen name from index
        self.CurrentScreen = self.__screens[index]['Name']

    # show_screen_name()
    def show_screen_name(self, name):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f"Screen with name {name} does not exist")
            return

        scr = [screen for screen in self.__screens if screen['Name'] == name][0]
        text = (TemplateString.resolve_template_string(scr['Text'][0], self.__client),TemplateString.resolve_template_string(scr['Text'][1], self.__client))
        self.Text = text
        self.__current_screen = scr['Name']

    # change_screen_text()
    def change_screen_text(self, name, text):
        if len([screen['Name'] for screen in self.__screens if screen['Name'] == name]) <= 0:
            print(f"Screen with name {name} does not exist")
            return

        next(s for s in self.__screens if s["Name"] == name)["Text"] = text
        if self.CurrentScreen == name:
            self.show_screen_name(name)

    # ----------------------------------------------------------
    # ----------------------------------------------------------



    # ----------------------------------------------------------
    # Properties -----------------------------------------------
    # ----------------------------------------------------------
    
    # --- Display Text ----------------------------------------------------------
    @property
    def Text(self):
        return self.__text
    @Text.setter
    def Text(self, new_text):
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

    # ----------------------------------------------------------
    # ----------------------------------------------------------

    def __del__(self):
        self.show_screen_index(0)

import re
from lxml import etree
from helpers.event_handler import EventHandler

class TemplateString(object):
    __eh = EventHandler()

    def resolve_value_template(xml):
        if xml.attrib['type'] == 'number':
            decimals = 4
            if xml.attrib['decimals'] != None:
                decimals = xml.attrib['decimals']
            return f'{xml.text:.{decimals}}'


    def resolve_opcua_template(xml, client):
        #TemplateString.__eh(None, {'node' : xml.attrib['node']})
        node_val = client.get_node(f'ns=2;s={xml.attrib["node"]}').get_value()
        decimals = 4
        if xml.attrib['decimals'] != None:
            decimals = xml.attrib['decimals']
        return f'{node_val:.{decimals}}'

    def resolve_template_string(templ, client):
        # Check if template string is present
        match_str = '<.*>'
        m = re.search(match_str, templ)
        if m == None:
            return templ

        xml = ''
        try:
            xml = etree.XML(m.group())
        except Exception as ex:
            print(f'Given template string "{templ}" was not valid: {ex}')
            return templ
    
        resolved_str = ''

        if xml.tag == 'value':
            resolved_str = TemplateString.resolve_value_template(xml)

        if xml.tag == 'opcua':
            resolved_str = TemplateString.resolve_opcua_template(xml, client)

        str_front = templ.split(m.group())[0]
        str_back  = templ.split(m.group())[1]
        return str_front + resolved_str + str_back

    @property
    def ResolveOPCUA():
        return TemplateString.__eh