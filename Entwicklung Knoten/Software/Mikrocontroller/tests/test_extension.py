#!/usr/bin/python

import sys, smbus2, time
from weakref import ref
import RPi.GPIO as GPIO

sys.path.append("../lib")
from extension import Microcontroller, UCException, Prescaler, RefVoltage

UC_ADR          = 100
UC_RESET_PIN    = 10




def throws_exception(func, exception):
    if isinstance(exception, type):
        try: func()
        except exception as ex: return True

    else: # Exception-Instanz Comparator nutzen?
        try: func()
        except type(exception) as ex: return ex == exception
    
    raise Exception(f"Erwartet, dass '{func}' eine '{exception}'-Exception wirft")





class TestMicrocontroller:   
    def setup_method(self): 
        bus       = smbus2.SMBus(1)
        self.__uc = Microcontroller(bus, UC_RESET_PIN, UC_ADR)

    def teardown_method(self): 
        GPIO.cleanup()
    
    def test_reachability(self): 
    
        ## TEST MIKROCONTROLLER DEAKTIVIERT -> System muss IO Error liefern
        self.__uc.enable(False)
        assert throws_exception(lambda: self.__uc.heartbeat([1,2,3,4]), OSError)
    
        ## TEST MIKROCONTROLLER AKTIVIERT -> Mikrocontroller Heartbeat muss mit gleichen Daten antworten, wie gesendet
        self.__uc.enable(True)
        assert self.__uc.heartbeat([1,2,3,4]) == [1,2,3,4]
    
    
    def test_buffer(self):
        IIC_RECV_BUFFER_SIZE = 16
        IIC_SEND_BUFFER_SIZE =  8
       
        # Zum Testen wird angenommen, dass der IIC-Empfangspuffer > als der IIC-Sendepuffer, sodass der Heartbeat
        # Mikrocontroller-Empfangspuffer -> [cmd, data0, data1,   ...]   -> Es können also IIC_RECV_BUFFER_SIZE - 1 Bytes empfangen werden
        # Mikrocontroller-Sendepuffer    -> [data0, data1, data2, ...]   -> Es können also IIC_SEND_BUFFER_SIZE     Bytes gesendet werden
        # Um den Buffer Overflow beim Sendepuffer testen zu können, muss also der Sendepuffer zwingend kleiner als der Empfangspuffer sein
        assert IIC_SEND_BUFFER_SIZE < IIC_RECV_BUFFER_SIZE - 1
    
        self.__uc.enable(True)
    
        ## TESTFALL 1: Keine Daten gesendet/empfangen
        assert self.__uc.heartbeat([]) == [] # Keine Sende Daten -> Zurückgesendete Daten auch leer
        
        ## TESTFALL 2: Sendepuffer des Mikrocontrollers vollständig füllen
        data = [i for i in range(IIC_SEND_BUFFER_SIZE)]
        assert self.__uc.heartbeat(data) == data
        
        ## TESTFALL 3: Sendepuffer des Mikrocontrollers läuft über
        data = [i for i in range(IIC_SEND_BUFFER_SIZE + 1)]
        assert throws_exception(lambda: self.__uc.heartbeat(data) == data, UCException(UCException.IIC_BUFFER_OVERFLOW))
    
        # TESTFALL 4: Empfangspuffer des Mikrocontrollers läuft über -> Mikrocontroller liefert NACK beim Überlauf
        data = [i for i in range(IIC_RECV_BUFFER_SIZE + 1)]
        assert throws_exception(lambda: self.__uc.heartbeat(data) == data, OSError)

    def test_ios(self):
        # Fuer diesen Test muessen jeweils 2 Partner-Pins miteinander verbunden werden. Der Test schaltet jeweils einen Pin als Input, den anderen als Output
        # und testet alle funktionalitaeten durch. Anschliessend werden die Pins in Ihrer Funktion getauscht getestet.

        pairs                   = [(0,1), (2,3)] # GPIO-Paare, welche verbunden sind (testen sich gegenseitig)
        ANALOG_HIGH_THRESHOLD   = 1023 - 50
        ANALOG_LOW_THRESHOLD    =    0 + 50
        presc                   = Prescaler.P128
        ref                     = RefVoltage.V5

        self.__uc.enable(True)
        time.sleep(1)

        for a,b in pairs:
             for i in range(2):
                self.__uc.input(a)                      # Pin A auf input stellen
                 
                self.__uc.output(b, True)               # Pin B auf high ziehen
                assert self.__uc.input(a) == True       # Da verbunden -> Pin A sollte jetzt high sein
                assert self.__uc.sample(a, presc, ref) >= ANALOG_HIGH_THRESHOLD # Auch Analog-Funktion testen

                self.__uc.output(b, False)              # Pin B auf output stellen und Pin auf low ziehen
                assert self.__uc.input(a) == False      # Pin A sollte jetzt low sein
                assert self.__uc.sample(a, presc, ref) <= ANALOG_LOW_THRESHOLD 

                self.__uc.input(b, True)                # B als Input, jedoch mit Pullup 
                assert self.__uc.input(a) == True       # A sollte durch Pullup jetzt wieder high sein
                assert self.__uc.sample(a, presc, ref) >= ANALOG_HIGH_THRESHOLD 

                a,b = b,a                               # Pins tauschen und nochmal in umgekehrter Reihenfolge testen




 