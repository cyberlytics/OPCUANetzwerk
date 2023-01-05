#!/usr/bin/python

import time, smbus2, struct
import RPi.GPIO as GPIO
from enum import Enum

DEBUG = False

class UCException(Exception):
    GENERAL_OK						=   0
    UNKNOWN_ERROR					=   1
    NOT_IMPLEMENTED					=   2

    TASK_NO_MORE_RESSOURCES			=  10
    TASK_ALREADY_RUNNING			=  11
    TASK_NOT_RUNNING				=  12
    								   
    IIC_INVALID_ADDRESS				=  20
    IIC_BUFFER_OVERFLOW				=  21
    IIC_BUFFER_EMPTY				=  22
    
    IOPIN_NOT_AN_IOPIN				=  30
    
    ADCPIN_NOT_AN_ADCPIN			=  40
    ADCPIN_INVALID_PRESCALER		=  41
    ADCPIN_INVALID_REF_VOLTAGE		=  42
    
    GPIO_NOT_EXISTING				=  50
    GPIO_FUNCTION_UNKNOWN			=  51
    GPIO_CALL_INVALID				=  52

    PWMPIN_NOT_AN_PWMPIN			=  60
    PWMPIN_USED_BY_OTHER_INSTANCE	=  61
    PWMPIN_FREQUENCY_OUT_OF_RANGE	=  62


    def __init__(self, error:int):
        self.__error = error
        super().__init__(__class__.error_to_text(error))

    @property
    def error(self) -> int:  return self.__error

    def __eq__(self, other) -> bool: 
        if isinstance(other, UCException) and other.error == self.error: return True
        return False 

    @classmethod 
    def error_to_text(cls, error:int) -> str:
        prefix = f"[{error}]"
        if error == cls.GENERAL_OK:                     return f"{prefix} Kein Fehler"
        if error == cls.UNKNOWN_ERROR:                  return f"{prefix} Ein unbekannter Fehler ist aufgetreten"
        if error == cls.NOT_IMPLEMENTED:                return f"{prefix} Es wurde eine Funktion aufgerufen, welche noch nicht implementiert wurde"

        if error == cls.TASK_NO_MORE_RESSOURCES:        return f"{prefix} Auf dem Mikrocontroller konnte ein Task aufgrund fehlender Ressourcen nicht gestartet werden"
        if error == cls.TASK_ALREADY_RUNNING:           return f"{prefix} Auf dem Mikrocontroller wurde versucht, einen Task mehrfach zu starten"
        if error == cls.TASK_NOT_RUNNING:               return f"{prefix} Auf dem Mikrocontroller wurde versucht, einen nicht gestarteten Task zu stoppen"

        if error == cls.IIC_INVALID_ADDRESS:            return f"{prefix} Auf dem Mikrocontroller wurde eine ungueltige IIC-Adresse konfiguriert"
        if error == cls.IIC_BUFFER_OVERFLOW:            return f"{prefix} Auf dem Mikrocontroller kam es zu einem Buffer overflow im I2C Sende-/Empfangsbuffer"
        if error == cls.IIC_BUFFER_EMPTY:               return f"{prefix} Aufruf hat einen Parameter erwartet, welcher nicht mitgesendet wurde"

        if error == cls.IOPIN_NOT_AN_IOPIN:             return f"{prefix} Der konfigurierte Pin auf dem Mikrocontroller besitzt nicht die Funktion 'IOPin'"

        if error == cls.ADCPIN_NOT_AN_ADCPIN:           return f"{prefix} Der konfigurierte Pin auf dem Mikrocontroller besitzt nicht die Funktion 'ADCPin'"
        if error == cls.ADCPIN_INVALID_PRESCALER:       return f"{prefix} Beim ADC-Sampling Aufruf wurde ein falscher Prescaler-Wert spezifiziert"
        if error == cls.ADCPIN_INVALID_REF_VOLTAGE:     return f"{prefix} Beim ADC-Sampling Aufruf wurde eine falsche Referenzspannung spezifiziert"

        if error == cls.GPIO_NOT_EXISTING:              return f"{prefix} Der per IIC angegebene GPIO-Pin existiert nicht"
        if error == cls.GPIO_FUNCTION_UNKNOWN:          return f"{prefix} Die per IIC angegebene Funktion kann auf diesem Pin nicht ausgefuehrt werden"
        if error == cls.GPIO_CALL_INVALID:              return f"{prefix} Der IIC Frameaufbau war fehlerhaft. Parameter stimmen nicht mit dem RPC Call ueberein"

        if error == cls.PWMPIN_NOT_AN_PWMPIN:			return f"{prefix} Der konfigurierte Pin auf dem Mikrocontroller besitzt nicht die Funktion 'PWMMPin'"
        if error == cls.PWMPIN_USED_BY_OTHER_INSTANCE:  return f"{prefix} Der zugrunde liegende Timer wird bereits auf einem anderen Pin verwendet"
        if error == cls.PWMPIN_FREQUENCY_OUT_OF_RANGE:  return f"{prefix} Die angegebene Ton-Frequenz kann nicht dargestellt werden"


        return f"{prefix} Fehler konnnte nicht zugeordnet werden"

    @classmethod
    def raise_if_error(cls, error:int):
        if error != cls.GENERAL_OK: raise cls(error)

class RefVoltage(Enum):
    V5   = 0b00 << 6
    V1_1 = 0b10 << 6

class Prescaler(Enum): # Bei 8MHz CPU Takt:
    P2   = 0b001 #   3.25uS
    P4   = 0b010 #   6.50uS
    P8   = 0b011 #  13.00uS
    P16  = 0b100 #  26.00uS
    P32  = 0b101 #  52.00uS
    P64  = 0b110 # 104.00uS
    P128 = 0b111 # 208.00uS



class Microcontroller:
    __ON_DELAY_SEC          =  .5 # wie viele Sekunden der Mikrocontroller braucht, bis er hochgefahren ist
    
    __HEARTBEAT             =   1

    __IOPIN_DIGITAL_IN      =  10
    __IOPIN_DIGITAL_OUT     =  11

    __ADCPIN_SAMPLE         =  20

    __PWMPIN_PLAY_FREQUENCY =  30

    def __init__(self, bus, reset_pin, address):
        self.__rst = reset_pin
        self.__bus = bus
        self.__adr = address
        self.__en  = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__rst, GPIO.OUT)
        self.enable(False)

    @property
    def address(self)   -> int:     return self.__adr
    @property
    def reset_pin(self) -> int:     return self.__rst
    @property
    def enabled(self)   -> bool:    return self.__en



    ### ENABLE MICROCONTROLLER ###
    def enable(self, enable:bool): 
        if enable == self.enabled: return

        GPIO.output(self.__rst, enable)
        self.__en = enable
        time.sleep(__class__.__ON_DELAY_SEC)



    ### HEARDBEAT (Mikrocontroller sendet gleichen Inhalt zurueck) ###
    def heartbeat(self, data): return list(self.__send_receive(__class__.__HEARTBEAT, len(data), bytearray(data)))


    ### Konfiguriert einen Pin als Input (ggf. mit Pullup-Widerstand) und Liest dessen digitalen Wert aus ###
    def input(self, pin:int, pullup:bool=None) -> bool:
        if pullup is None: return self.__call(__class__.__IOPIN_DIGITAL_IN, "<?", "<B",  pin)
        else:              return self.__call(__class__.__IOPIN_DIGITAL_IN, "<?", "<BB", pin, pullup)


    ### Konfiguriert einen Pin als Output und setzt dessen Wert auf High / Low
    def output(self, pin:int, value:bool): 
        self.__call(__class__.__IOPIN_DIGITAL_OUT, "", "<B?", pin, value)


    ### Startet eine ADC-Konversation mit eingestellten Prescaler/Referenzspannung und gibt dessen Wert zureuck
    def sample(self, pin:int, presc:Prescaler, ref:RefVoltage, pullup:bool=None) -> int:
        if pullup is None: return self.__call(__class__.__ADCPIN_SAMPLE, "<H", "<BBB",  pin, presc.value, ref.value)
        else:              return self.__call(__class__.__ADCPIN_SAMPLE, "<H", "<BBBB", pin, presc.value, ref.value, pullup)
    

    ### Spielt ein Rechtecksignal mit spezifizierter Frequenz auf einem definierten Pin ab (und beendet das Signal nach ggf. nach einer definierten Zeit) ###
    def playFrequency(self, pin:int, frequency:float, duration_us:int=None):
        if duration_us is None: self.__call(__class__.__PWMPIN_PLAY_FREQUENCY, "", "<Bf",  pin, frequency)
        else:                   self.__call(__class__.__PWMPIN_PLAY_FREQUENCY, "", "<BfI", pin, frequency, duration_us)


    ### Fuehrt einen Aufruf mit Sende/Rueckgabe Parametern durch
    def __call(self, cmd, fmat_receive, fmat_send, *args):
        try: send_data   = bytearray(struct.pack(fmat_send, *args))
        except Exception as ex: raise Exception(f"Aufrufparameter fuer Command '{cmd}' fehlerhaft. Erwartetes Format: '{fmat_send}', Parameter: {args}. Fehler: {ex}")

        recv_byte_len    = struct.calcsize(fmat_receive)
        recv_data        = self.__send_receive(cmd, recv_byte_len, send_data)

        try: recv_values = struct.unpack(fmat_receive, recv_data)
        except Exception as ex: raise Exception(f"Empfangsparameter fuer Command '{cmd}' fehlerhaft. Erwartetes Format: '{fmat_receive}', Daten: {recv_data}. Fehler: {ex}")

        if len(recv_values) == 0: return None
        if len(recv_values) == 1: return recv_values[0]
        return recv_values


    ### Kodiert eine Nachricht an den Mikrocontroller + prueft und dekotiert dessen Antwort
    def __send_receive(self, cmd:int, recv_byte_len:int, send_data:bytearray=[]) -> bytearray:
        # Nachrichtenaufbau:
        # chksm  |I2C Adr w + cmd +     sum(send_data)               + I2C Adr r + len +     sum(recv_data)     + err|         & 0xFF
        # len                                                                     |    len(recv_data)     +  1  +   1|
        #        [I2C Adr w] [cmd] [send_data0..send_dataX] |RESTART| [I2C Adr r] [len] [recv_data0..recv_dataX] [err] [chksm]

        req      = bytearray([cmd]) + send_data
        write    = smbus2.i2c_msg.write(self.__adr, req)
        read     = smbus2.i2c_msg.read(self.__adr, recv_byte_len + 3) # Empfangspaket um 3 Bytes erweitern: len, err, chksm

        self.__bus.i2c_rdwr(write, read)
        rsp      = bytearray(b for b in read)

        if DEBUG: print(f">>> UC MESSAGE: send [{len(req)}] ->{[int(b) for b in req]}<- receive [{len(rsp)}] ->{[int(b) for b in rsp]}<- <<<")

        # Antwortnachricht: [len] [data0...dataX] [err] [chksm]

        # Nachrichtenlaenge ermitteln
        rsp_size      = len(rsp)
        if rsp_size < 3: raise Exception(f"Paket '{req}|{rsp}' fragmentiert. Laengenbyte '{rsp_size}' muss > 2 sein") # Kleinste Antwortnachricht -> 1 lenbyte + 0 datenbytes + 1 errbyte + 1 chksmbyte
        rsp_size      = min(rsp_size - 1, rsp[0])

        # Nachrichtenbytes data0...dataX ermitteln
        recv_data = rsp[1:(rsp_size - 1)] # Ohne Laengenbyte und ohne err + chksm
        rsp_err   = rsp[(rsp_size - 1)]
        rsp_chk   = rsp[(rsp_size - 0)]

        # Checksumme pruefen
        #             ADR           w  + cmd + sum(send_data) +  I2C Adr           r  +   len    + sum(recv_data) +   err    & 0xFF
        chksm = ((self.__adr << 1 | 0) + cmd + sum(send_data) + (self.__adr << 1 | 1) + rsp_size + sum(recv_data) + rsp_err) & 0xFF
        if chksm != rsp_chk: raise Exception(f"Checksummenfehler: Erwartet: {chksm}, Tatsaechlich: {rsp_chk}")
        
        # Error-Code pruefen
        UCException.raise_if_error(rsp_err)
        if len(recv_data) != recv_byte_len: raise Exception(f"Bei Anfrage '{cmd}' an den Mikrocontroller wurde als Antwort {recv_byte_len} Bytes erwartet. Mikrocontroller hat jedoch mit {len(recv_data)} Bytes geantwortet")

        return recv_data

    def __str__(self)   -> str: return f"UC {self.address} [{'Enabled' if self.enabled else 'Disabled'}]"
    def __repr__(self)  -> str: return f"<{self}>"