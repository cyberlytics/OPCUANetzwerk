#!/usr/bin/python

import smbus2, sys

sys.path.append("../lib")
from extension  import Microcontroller, UCException, Prescaler, RefVoltage
from shenanigans import play

UC_ADR          = 100
UC_RESET_PIN    = 10


if __name__ == "__main__":
    bus  = smbus2.SMBus(1)
    uc   = Microcontroller(bus, UC_RESET_PIN, UC_ADR)


        
    SEQ_A  =    "f4:va , g4:va , c4:v  , g4:va , a4:va , c5:s  , b4:s , a4:a , f4:va , g4:va , c4:vva, a, a, c4:s, c4:s, d4:s, f4:a, f4:s," \
                "f4:va , g4:va , c4:v  , g4:va , a4:va , c5:s  , b4:s , a4:a , f4:va , g4:va , c4:vva, a, a, s, s, s, a, s," \
                "v, d4:a  , e4:a  , f4:a  , f4:a  , g4:a  , e4:as , d4:s , c4:ah, va    , d4:a  , d4:a  , e4:a, f4:a, d4:v, c4:a, c5:a, a, c5:a, g4:va, v," \
                "a, d4:a  , d4:a  , e4:a  , f4:a  , d4:a  , f4:a  , g4:a , a, e4:a, d4:a, c4:va, va, d4:a, d4:a, e4:a, f4:a, d4:a, c4:v," \
                "g4:a, g4:a, g4:a, a4:a, g4:v, v, f4:ha, g4:a, a4:a, f4:a, g4:a, g4:a, g4:a, a4:a, g4:v, c4:v," \
                "h, d4:a, e4:a, f4:a, d4:a, a, g4:a, a4:a, g4:va, c4:s, d4:s, f4:s, d4:s, a4:as, a4:as, g4:va, c4:s, d4:s, f4:s, d4:s, " \
                "g4:as, g4:as, f4:as, e4:s, d4:a, c4:s, d4:s, f4:s, d4:s, f4:v, g4:a, e4:as, d4:s, c4:a, c4:a, c4:a, g4:v, f4:h, c4:s, d4:s, f4:s, d4:s, " \
                "a4:as, a4:as, g4:va, c4:s, d4:s, f4:s, d4:s, c5:v, e4:a, f4:as, e4:s, d4:a, c4:s, d4:s, f4:s, d4:s, f4:v, g4:a, e4:as, d4:s, c4:v, c4:a, " \
                "g4:v, f4:h"
    
    uc.enable(True)
    play(uc, 4, SEQ_A, 150, .9)