import time
import helpers.globals as globals
from helpers.menu import Menu
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

globals.init()

globals.lcd.set_backlight(True)
globals.lcd.add_screen('sensor1' , ('Tempe.: xx.x°C','Luftf.: xx.x%'))
globals.lcd.add_screen('sensor2', ('Luftd.: xx.x°C','Luftq.: xx.xppm'))
globals.lcd.add_screen('opcua'  , ('Das ist ein','OPCUA-Screen'))
globals.lcd.show_screen_name('opcua')

menu = Menu()

#buttons = Buttons()
#buttons.Button1.start_measurement()
#buttons.Button4.start_measurement()

#def cb_bd(sender, args):
#    print("ButtonDown")
#    if (lcd.CurrentScreen == '' or lcd.CurrentScreen == 'sensor'):
#        lcd.show_screen_name('opcua')
#    elif (lcd.CurrentScreen ==  'opcua'):
#        lcd.show_screen_name('sensor')

#lcd.show_screen_name('sensor')

#def cb_bu(sender, args):
#    print("ButtonUp")

#def cb_bs(sender, args):
#    print("ButtonStay")

#start_time = 0
#def time_start(sender, args):
#    print("Time start")
#    global start_time
#    start_time = time.time()

#def time_measure(sender, args):
#    global start_time
#    time_diff = time.time() - start_time
#    print(f"{time_diff:.2f}")

#def time_end(sender, args):
#    global start_time
#    start_time = 0
#    print("Time end")

#buttons.Button1.ButtonDown.subscribe(cb_bd)
##buttons.Button1.ButtonStay.subscribe(cb_bs)
#buttons.Button1.ButtonUp.subscribe(cb_bu)

#buttons.Button4.ButtonDown.subscribe(time_start)
#buttons.Button4.ButtonStay.subscribe(time_measure)
#buttons.Button4.ButtonUp.subscribe(time_end)

#while True:
#    #print(buttons.Button1.status)
#    t = bme280.temperature
#    h = bme280.humidity
#    text = (f'Tempe.: {t[0]:.2f}°C', f'Luftf.: {h[0]:.2f}%')
#    lcd.change_screen_text('sensor', text)
#    time.sleep(1)