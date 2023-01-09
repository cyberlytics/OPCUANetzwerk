#!/usr/bin/python

import sys, smbus2, time, struct
import RPi.GPIO as GPIO

sys.path.append("../lib")
from extension import Microcontroller, UCException, Prescaler, RefVoltage
from shenanigans import play

UC_ADR          = 100
UC_RESET_PIN    = 10

def throws_exception(func, exception):
    if isinstance(exception, type):
        try: func()
        except exception as ex: return True

    else: # Exception-Instanz Comparator nutzen?
        try: func()
        except type(exception) as ex: 
            return ex == exception
    
    return False





class TestMicrocontroller:   
    def setup_method(self): 
        self.__bus  = smbus2.SMBus(1)
        self.__uc   = Microcontroller(self.__bus, UC_RESET_PIN, UC_ADR)
        self.__call = getattr(self.__uc, "_Microcontroller__call")

    def teardown_method(self): 
        self.__uc.enable(False) # Mikrocontroller resetten
        GPIO.cleanup()


    def print_header(self, txt):
        txt = f"### >>> {txt} <<< ###"
        sep = "".join("-" for i in range(len(txt)))

        print("\n\n")
        print(sep)
        print(txt)
        print(sep)
    


    def test_reachability(self): 
        self.print_header("TESTE ERREICHBARKEIT")
    
        ## TEST MIKROCONTROLLER DEAKTIVIERT -> System muss IO Error liefern
        print(f"Teste Erreichbarkeit Mikrocontroller im Ausgeschalenen Zustand")
        self.__uc.enable(False)
        assert throws_exception(lambda: self.__uc.heartbeat([1,2,3,4]), OSError)
    
        ## TEST MIKROCONTROLLER AKTIVIERT -> Mikrocontroller Heartbeat muss mit gleichen Daten antworten, wie gesendet
        print(f"Teste Erreichbarkeit Mikrocontroller im Eingeschaltenen Zustand")
        self.__uc.enable(True)
        assert self.__uc.heartbeat([1,2,3,4]) == [1,2,3,4]
    

    
    #def test_iic_buffer(self):
    #    self.print_header("TESTE IIC-BUFFER")
    #
    #    IIC_BUFFER_SIZE = 16
    #   
    #    # Mikrocontroller-Empfangspuffer -> [cmd, data0, data1,   ...]   -> Es können also IIC_RECV_BUFFER_SIZE - 1 Bytes empfangen werden
    #    # Mikrocontroller-Sendepuffer    -> [data0, data1, data2, ...]   -> Es können also IIC_SEND_BUFFER_SIZE     Bytes gesendet werden
    #
    #    self.__uc.enable(True)
    #
    #    ## TESTFALL 1: Keine Daten gesendet/empfangen
    #    print("Teste Leere Datenuebertragung")
    #    assert self.__uc.heartbeat([]) == [] # Keine Sende Daten -> Zurückgesendete Daten auch leer
    #    
    #    ## TESTFALL 2: Empfangspuffer des Mikrocontrollers vollständig füllen
    #    print("Teste vollstaendig gefuellten Sendepuffer des Mikrocontrollers")
    #    data = [i for i in range(IIC_BUFFER_SIZE - 1)]
    #    assert self.__uc.heartbeat(data) == data
    #    
    #    # TESTFALL 3: Empfangspuffer des Mikrocontrollers läuft über -> Mikrocontroller liefert NACK beim Überlauf
    #    print("Teste Empfangspufferueberlauf")
    #    data = [i for i in range(IIC_BUFFER_SIZE)]
    #    assert throws_exception(lambda: self.__uc.heartbeat(data) == data, OSError)




    def test_iic_protocol(self):
        self.print_header("TESTE I2C Protokoll")
        
        PWM_PIN   = 4
        
        self.__uc.enable(True)
        
        # Mikrocontroller sollte erreichbar sein -> Teste daher als erstes, ob Heartbeat funktioniert
        assert self.__uc.heartbeat([1,2,3,4]) == [1,2,3,4]
        
        # I2C Adresse zwar korrekt, jedoch nach Start "Read" Aufforderung -> Mikrocontroller sollte mit NACK (oder auch "nicht") antworten
        assert throws_exception(lambda: self.__bus.read_byte(UC_ADR), OSError)
        
        # Teste Abbruch -> Baue Sende-Nachricht bis Restart korrekt auf, sende jedoch statt restart stop -> Funktion sollte nicht aufgerufen werden
        print("Teste Abbruch-Funktion -> !!!ES SOLLTE KEIN TON HOERBAR SEIN!!!")
        send_data = bytearray(struct.pack("<BBf", getattr(Microcontroller, "_Microcontroller__PWMPIN_PLAY_FREQUENCY"), PWM_PIN, 440))
        write     = smbus2.i2c_msg.write(UC_ADR, send_data)
        self.__bus.i2c_rdwr(write)
        time.sleep(2)
        
        
        
        # Selbe Test, doch diesmal mit Restart
        print("JETZT SOLLTE EIN TON HOERBAR SEIN")
        read      = smbus2.i2c_msg.read(UC_ADR, 1) 
        self.__bus.i2c_rdwr(write, read)
        time.sleep(2)
        
        print("TON AUS")
        self.__uc.playFrequency(PWM_PIN, 0) # Ton wieder abschalten
        time.sleep(2)
         
        
        
        # Sollte auch funktionieren, wenn Restart-Adresse falsch ist (Restart Signal soll Prozedur triggern)
        print("JETZT SOLLTE EIN TON HOERBAR SEIN")
        read      = smbus2.i2c_msg.read(UC_ADR+1, 1) 
        assert throws_exception(lambda: self.__bus.i2c_rdwr(write, read), OSError) # Nach Restart antwortet natuerlich keiner -> OSError
        time.sleep(2)
         
        print("TON AUS")
        self.__uc.playFrequency(PWM_PIN, 0) # Ton wieder abschalten
        
        
        # Checksumme pruefen
        #                                                                  Byte:                        0      1      2       3  ...  8       9        10  
        # [I2C Adr + Write] [CMD-Heartbeat] [dbl0] [dbl1] [dbl...] [dbl7] |RESTART| [I2C Adr + Read ] [len] [dbl0] [dbl1] [dbl...] [dbl7] [Error=0] [Chksm]
        # [UC_ADR << 1 | 0] [      cmd    ] [         send_data         ] |         [UC_ADR << 1 | 1] [                     read_data                     ]
    
        dbl_val    = 3.1415
        cmd        = getattr(Microcontroller, "_Microcontroller__HEARTBEAT")
        send_data  = bytearray(struct.pack("<d", dbl_val))
        write      = smbus2.i2c_msg.write(UC_ADR, bytearray([cmd]) + send_data)
        read       = smbus2.i2c_msg.read(UC_ADR, 11)
        self.__bus.i2c_rdwr(write, read) 
        read_data  = bytearray(b for b in read)
    
        assert len(read_data) == 11                     # len, dbl0-7, err, chksm
        assert read_data[9]   == UCException.GENERAL_OK # Error = GENERAL_OK
        assert read_data[0]   == 10                     # len = 10
        # Checksum                I2C Adr      | w  + cmd +  send_data     +  I2C Adr     | R  +len +                +Err
        assert read_data[10]  == ((UC_ADR << 1 | 0) + cmd + sum(send_data) + (UC_ADR << 1 | 1) + 10 + sum(send_data) + 0  ) & 0xff;
        assert struct.unpack("<d", read_data[1:9])[0] == dbl_val


        
    # Testet die PWM Funktionalitaet 
    def test_PWMPin(self):
        self.print_header("TESTE PWMPin Funktionalitaet")
    
        pin                     = 4
        MIN_FREQ                = 50.0
        MAX_FREQ                = 16e3
    
        self.__uc.enable(True)
    
        print("Teste RPC Schnittstelle playFrequency") # Aufbau: pin(byte) freq(float) [dur(uint32_t)]
        cmd = getattr(self.__uc, "_Microcontroller__PWMPIN_PLAY_FREQUENCY")
        assert throws_exception(lambda: self.__call(cmd, "", ""),                           UCException(UCException.IIC_BUFFER_EMPTY))              # Pin vergessen -> Mikrocontroller sollte mit IIC_BUFFER_EMPTY antworten
        assert throws_exception(lambda: self.__call(cmd, "", "<B",    pin),                 UCException(UCException.IIC_BUFFER_EMPTY))              # Nur Pin -> Frequenz required 
        assert throws_exception(lambda: self.__call(cmd, "", "<BH",   pin, 440),            UCException(UCException.IIC_BUFFER_EMPTY))              # Frequenz Fragmentiert
        self.__call(cmd, "", "<Bf",  pin, 440.0)                                                                                                    # Aufruf mit Pin und Frequenz sollte funktionieren (dur optional)
        assert throws_exception(lambda: self.__call(cmd, "", "<BfH",  pin, 880.0, 1000),    UCException(UCException.IIC_BUFFER_EMPTY))              # Duration Fragmentiert
        self.__call(cmd, "", "<BfI", pin, 880.0, 1000)                                                                                              # Aufruf mit Frequenz und Dauer
        assert throws_exception(lambda: self.__call(cmd, "", "<BfIB", pin, 880.0, 1000, 1), UCException(UCException.GPIO_CALL_INVALID))             # Zu viele Parameter angegeben
    
        self.__uc.playFrequency(pin, 0) # Ton aus
        time.sleep(2)
    
    
        print("Teste Fehlerfaelle")
        assert throws_exception(lambda: self.__uc.playFrequency(6, 440),                    UCException(UCException.GPIO_NOT_EXISTING))             # Teste nicht vorhandenen Pin
        assert throws_exception(lambda: self.__uc.playFrequency(1, 440),                    UCException(UCException.GPIO_FUNCTION_UNKNOWN))         # Teste Pin unterstuetzt kein PWM
        
        print("Teste Frequenzbereiche")
        assert throws_exception(lambda: self.__uc.playFrequency(pin, -1),                   UCException(UCException.PWMPIN_FREQUENCY_OUT_OF_RANGE)) # Teste Negative Frequenz
        assert throws_exception(lambda: self.__uc.playFrequency(pin, MIN_FREQ - 1),         UCException(UCException.PWMPIN_FREQUENCY_OUT_OF_RANGE)) # Teste Ton < erlaubte Frequenz
        self.__uc.playFrequency(pin, MIN_FREQ)
        self.__uc.playFrequency(pin, 440)
        self.__uc.playFrequency(pin, MAX_FREQ)
        assert throws_exception(lambda: self.__uc.playFrequency(pin, MAX_FREQ + 1),         UCException(UCException.PWMPIN_FREQUENCY_OUT_OF_RANGE)) # Teste Ton < erlaubte Frequenz
    
        self.__uc.playFrequency(pin, 0)
        time.sleep(2)
    
    
        ### Ab hier muss der Anwender "mithoeren"
    
        ## Teste Frequenz + Delay Time
        print("Jetzt sollte ein Ton mit 440Hz fuer 2 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 440, 2_000_000)
        time.sleep(2)
        print("Jetzt sollte der Ton erloschen sein")
        time.sleep(2)
    
        # Test Endlos Ton + Beenden ueber Pi 
        print("Jetzt sollte ein Ton mit 880Hz fuer 2 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 880)
        time.sleep(2)
        print("Jetzt sollte der Ton erloschen sein")
        self.__uc.playFrequency(pin, 0)
        time.sleep(2)


        # Test Laufenden Endlos Ton überschreiben
        print("Jetzt sollte ein Ton mit 440Hz fuer 2 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 440)
        time.sleep(2)
        print("Jetzt sollte ein Ton mit 880Hz fuer 2 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 880, 2_000_000)
        time.sleep(2)
        print("Jetzt sollte der Ton erloschen sein")
        time.sleep(2)

        # Test Laufenden Begrenzten Ton überschreiben
        print("Jetzt sollte ein Ton mit 440Hz fuer 2 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 440, 3_000_000)
        time.sleep(2)
        print("Jetzt sollte ein Ton mit 880Hz fuer 4 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 880) #TODO: Scheint nicht zu funktionieren
        time.sleep(4)
        print("Jetzt sollte der Ton erloschen sein")
        self.__uc.playFrequency(pin, 0)
        time.sleep(2)

        # Teste gleichen Ton delay überschreiben
        print("Jetzt sollte ein Ton mit 440Hz fuer 4 Sekunden hoerbar sein")
        self.__uc.playFrequency(pin, 440, 3_000_000)
        time.sleep(2)
        self.__uc.playFrequency(pin, 440, 2_000_000) #TODO: Scheint nicht zu funktionieren
        time.sleep(2)
        print("Jetzt sollte der Ton erloschen sein")
        time.sleep(2)


    def test_IOPin(self):
        self.print_header("TESTE IOPin Funktionalitaet")
    
        # Fuer diesen Test muessen jeweils 2 Partner-Pins miteinander verbunden werden. Der Test schaltet jeweils einen Pin als Input, den anderen als Output
        # und testet alle funktionalitaeten durch. Anschliessend werden die Pins in Ihrer Funktion getauscht getestet.
    
        invalid_pin             = 6
        pairs                   = [(0,1), (2,3)]    # GPIO-Paare, welche verbunden sind (testen sich gegenseitig)
    
        self.__uc.enable(True)

        print("Teste RPC Schnittstelle output") # Aufbau: pin(byte) value(bool)
        pin = pairs[0][0]
        cmd = getattr(self.__uc, "_Microcontroller__IOPIN_DIGITAL_OUT")
        assert throws_exception(lambda: self.__call(cmd, "", ""),                           UCException(UCException.IIC_BUFFER_EMPTY))              # Pin vergessen -> Mikrocontroller sollte mit IIC_BUFFER_EMPTY antworten
        assert throws_exception(lambda: self.__call(cmd, "", "<B",    pin),                 UCException(UCException.IIC_BUFFER_EMPTY))              # Nur Pin -> value required 
        self.__call(cmd, "", "<B?",  pin, False)                                                                                                      # Korrekter aufruf
        assert throws_exception(lambda: self.__call(cmd, "", "<B?B",  pin, False, 1),       UCException(UCException.GPIO_CALL_INVALID))             # Zu viele Parameter angegeben

        print("Teste RPC Schnittstelle input") # Aufbau: pin(byte) [pullup(bool)] -> bool
        cmd = getattr(self.__uc, "_Microcontroller__IOPIN_DIGITAL_IN")
        assert throws_exception(lambda: self.__call(cmd, "", ""),                           UCException(UCException.IIC_BUFFER_EMPTY))              # Pin vergessen -> Mikrocontroller sollte mit IIC_BUFFER_EMPTY antworten
        self.__call(cmd, "<?", "<B",   pin)                                                                                                         # Korrekter aufruf
        self.__call(cmd, "<?", "<B?",  pin, True)                                                                                                   # Korrekter aufruf mit optionalen Parameter pullup
        assert throws_exception(lambda: self.__call(cmd, "", "<B?B",  pin, False, 1),       UCException(UCException.GPIO_CALL_INVALID))             # Zu viele Parameter angegeben

    
        #Teste Fehlerfälle
        print("Teste Fehlerfaelle")
        assert throws_exception(lambda: self.__uc.input(invalid_pin),                       UCException(UCException.GPIO_NOT_EXISTING))
        assert throws_exception(lambda: self.__uc.output(invalid_pin, False),               UCException(UCException.GPIO_NOT_EXISTING))
        
        print("Teste Hardware-Pins")
        for a,b in pairs:
            # Iteration 1 -> a = input, b = output | Iteration 2 -> a = output, b = input
             for i in range(2):
                self.__uc.input(a)                      # Pin A auf input stellen
                
                self.__uc.output(b, True)               # Pin B auf high ziehen
                assert self.__uc.input(a) == True       # Da verbunden -> Pin A sollte jetzt high sein
        
                self.__uc.output(b, False)              # Pin B auf output stellen und Pin auf low ziehen
                assert self.__uc.input(a) == False      # Pin A sollte jetzt low sein
        
                self.__uc.input(b, True)                # B als Input, jedoch mit Pullup 
                assert self.__uc.input(a) == True       # A sollte durch Pullup jetzt wieder high sein
        
                a,b = b,a                               # Pins tauschen und nochmal in umgekehrter Reihenfolge testen



    def test_ADCPin(self):
        self.print_header("TESTE ADCPin Funktionalitaet")
    
        # Fuer diesen Test muessen jeweils 2 Partner-Pins miteinander verbunden werden. Der Test schaltet jeweils einen Pin als Input, den anderen als Output
        # und testet alle funktionalitaeten durch. Anschliessend werden die Pins in Ihrer Funktion getauscht getestet.
    
        invalid_pin             = 6
        pairs                   = [(0,1), (2,3)]    # GPIO-Paare, welche verbunden sind (testen sich gegenseitig)
        ANALOG_HIGH_THRESHOLD   = 1023 - 50         # Toleranz, in der der ADC-Wert für HIGH / LOW liegen muss
        ANALOG_LOW_THRESHOLD    =    0 + 50
        presc                   = Prescaler.P128    # Sampling Prescaler
        ref                     = RefVoltage.V5     # Mess Referenzspannung
    
        self.__uc.enable(True)

        print("Teste RPC Schnittstelle sample") # Aufbau: pin(byte) prescaler(byte) ref(byte) -> uint16_t
        pin = pairs[0][0]
        cmd = getattr(self.__uc, "_Microcontroller__ADCPIN_SAMPLE")
        assert throws_exception(lambda: self.__call(cmd, "<H", ""),                                       UCException(UCException.IIC_BUFFER_EMPTY))            # Pin vergessen -> Mikrocontroller sollte mit IIC_BUFFER_EMPTY antworten
        assert throws_exception(lambda: self.__call(cmd, "<H", "<B", pin),                                UCException(UCException.IIC_BUFFER_EMPTY))            # nur Pin spezifiziert -> prescaler und ref required
        assert throws_exception(lambda: self.__call(cmd, "<H", "<BB", pin, presc.value),                  UCException(UCException.IIC_BUFFER_EMPTY))            # Pin + prescaler spezifiziert -> ref required
        self.__call(cmd, "<H", "<BBB", pin, presc.value, ref.value)                                                                                             # Korrekter aufruf
        assert throws_exception(lambda: self.__call(cmd, "", "<BBBB", pin, presc.value, ref.value, 0),    UCException(UCException.GPIO_CALL_INVALID))           # Zu viele Parameter angegeben

    
        #Teste Fehlerfälle
        print("Teste Fehlerfaelle")
        assert throws_exception(lambda: self.__uc.sample(invalid_pin, presc, ref),                        UCException(UCException.GPIO_NOT_EXISTING))
        assert throws_exception(lambda: self.__call(cmd, "<H", "<BBB", pin, 0b1000, ref.value),           UCException(UCException.ADCPIN_INVALID_PRESCALER))    # Ungültiger Prescaler
        assert throws_exception(lambda: self.__call(cmd, "<H", "<BBB", pin, presc.value, 0b11),           UCException(UCException.ADCPIN_INVALID_REF_VOLTAGE))  # Ungültige RefVoltage

        # Teste Existierenden Pin, jedoch ohne ADC Funktionalität (Pin 4 = PWMPin, kein ADCPin)
        assert throws_exception(lambda: self.__uc.sample(4, presc, ref),                                  UCException(UCException.GPIO_FUNCTION_UNKNOWN))


        print("Teste RevVoltage/Prescaler Values")
        a,b = pairs[0]
        self.__uc.output(b,False) # B als Output Low
        for prescaler in Prescaler:
            for ref_voltage in RefVoltage:
                assert self.__uc.sample(a, prescaler, ref_voltage) <= ANALOG_LOW_THRESHOLD 


        print("Teste Hardware-Pins")
        for a,b in pairs:
            # Iteration 1 -> a = input, b = output | Iteration 2 -> a = output, b = input
             for i in range(2):
                self.__uc.input(a)                      # Pin A auf input stellen
                self.__uc.output(b, True)               # Pin B auf high ziehen
                assert self.__uc.sample(a, presc, ref) >= ANALOG_HIGH_THRESHOLD # Analog-Funktion testen
     
                self.__uc.output(b, False)              # Pin B auf output stellen und Pin auf low ziehen
                assert self.__uc.sample(a, presc, ref) <= ANALOG_LOW_THRESHOLD 
        
                self.__uc.input(b, True)                # B als Input, jedoch mit Pullup 
                assert self.__uc.sample(a, presc, ref) >= ANALOG_HIGH_THRESHOLD 
        
                a,b = b,a                               # Pins tauschen und nochmal in umgekehrter Reihenfolge testen



    def test_shenanigans(self):
        self.print_header("TESTE SHENANIGANS")
    
        SEQ_A  =    "e4:v  , g4:a  , c5:v  , c5:v  , h4:a  , h4:v  , a4:aa , e4:va ,    a  , e4:v  , g4:a  ,"                           \
                    "a4:a  , a4:va , g4:va , g4:a  , h3:hv ,    a  , g3:a  , h4:a  , h4:v  , h4:ava, a4:a  ,"                           \
                    "g4:a  , g4:v  , g4:av , a     , h3:a  , g4:v  , f4:a  , d4:v  , e4:a"                                              \
                    "h     , a     , e5:v  , d5:a  , c5:v  , c5:v  , h4:a  , h4:v  , a4:aa , e4:va , t     , e4:t  , g4:t  ,"           \
                    "a4:a  , a4:v  , g4:av , g4:a  , h3:ahv,    v  ,"                                                                   \
                    "h4:v  , h4:a  , h4:ava, a4:a  , g4:v  , g4:a  , g4:av ,    a  , h3:a  , g4:a  , g4:v  , f4:av , d4:a  , c4:a"      \
                    "h     ,    h  ,    v  , c5:a  , a4:ava, c5:a  , h4:a  , g4:v  , g4:av , h4:a  , a4:a"                              \
                    "v     , f4:a  , d4:av , a4:v  , g4:hv ,    v  , f4:h  , f4:va , f4:a  ,"                                           \
                    "e4:v  , a4:a  , a4:av ,    v  , d4:a  , d4:va , e4:v  , f#4:a , g4:ah ,    a  , e5:v  , d5:a,"                     \
                    "c5:v  , c5:v  , h4:a  , h4:v  , a4:aa , e4:va ,    t  , e4:t  , g4:t  , a4:v  , a4:v  , g4:a  , g4:v  , h3:a"      \
                    "hv    ,    a  , h4:aa , h4:va , h4:a  , a4:a  , g4:a  , f4:a  ,"                                                   \
                    "e4:v  , g4:v  , g4:v  , e5:v  , d5:v  , a4:h  , h4:a  , g4:a  , c5:h  ,    h"
    
        self.__uc.enable(True)
        play(self.__uc, 4, SEQ_A, 180, .75)

