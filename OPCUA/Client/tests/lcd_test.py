import sys, time
sys.path.insert(0, '..')

import RPi.GPIO as GPIO
GPIO.setwarnings(False)

from actors.lcd_display import LcdDisplay

def test_add_screen():
    print('Fuege einen Screen hinzu')

    lcd = LcdDisplay()
    lcd.add_screen('test1', ('',''))
    assert lcd.ScreenCount == 1

def test_add_existing_screen():
    print('Fuege den gleichen Screen doppelt hinzu')

    lcd = LcdDisplay()
    lcd.add_screen('test1', ('',''))
    lcd.add_screen('test1', ('',''))
    assert lcd.ScreenCount == 1

def test_delete_existing_screen():
    print('Loesche vorhandenen Screen')

    lcd = LcdDisplay()
    lcd.add_screen('test1', ('',''))
    lcd.remove_screen('test1')
    assert lcd.ScreenCount == 0

def test_delete_not_existing_screen():
    print('Loesche nicht existierenden Screen')

    lcd = LcdDisplay()
    result = lcd.remove_screen('test1')
    assert result == False

def test_get_existing_screen():
    print('Hole existierenden Screen')

    lcd = LcdDisplay()
    lcd.add_screen('test1', ('X','Y'))
    screen = lcd.get_screen('test1')
    assert screen['Text'] == ('X','Y')

def test_alter_existing_screen():
    print('Veraendere existierenden Screen')

    lcd = LcdDisplay()
    lcd.add_screen('test1', ('X','Y'))
    lcd.change_screen_text('test1', ('1', '2'))
    screen = lcd.get_screen('test1')
    assert screen['Text'] == ('1','2')

def test_backlight_blink():
    print('LCD_Display sollte 5mal blinken')
    lcd = LcdDisplay()
    time.sleep(1)

    for i in range(5):
        lcd.set_backlight(True)
        time.sleep(0.5)
        lcd.set_backlight(False)
        time.sleep(0.5)

    lcd.set_backlight(True)

def test_update_functionality():
    print('Teste LCD Update Funktion')

    lcd = LcdDisplay()
    
    print('Update zweimal starten')
    result = lcd.start_update()
    result = lcd.start_update()

    assert result == False

    lcd.stop_update()