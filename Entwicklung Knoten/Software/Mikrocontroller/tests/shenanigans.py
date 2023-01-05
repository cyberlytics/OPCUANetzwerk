#!/usr/bin/python

import sys, re, time

NOTES          = { "c":0, "c#":1, "db":1, "d":2, "d#":3, "eb":3, "e":4, "f":5, "f#":6, "gb":6, "g":7, "g#":8, "ab":8, "a":9, "a#":10, "b":10, "h":11 }
NOTE_LETTERS   = "|".join(re.escape(n) for n in NOTES.keys())

LENGTHS        = { "g":1, "h":.5, "v":.25, "a":.125, "t": .5/3 }
LENGTH_LETTERS = "|".join(re.escape(l) for l in LENGTHS.keys())               
RE_NOTE        = re.compile(fr"^(?:({NOTE_LETTERS})(-?\d):)?((?:{LENGTH_LETTERS})+)$")

def convert_note(tone, bpm):
    nl,nh,ls  = RE_NOTE.match(tone).groups()
    
    if nl is not None and nh is not None:
        note_nr   = NOTES[nl] - 8 + int(nh) * 12
        freq      = 440 * (2 ** (1/12)) ** (note_nr - 49)
    else: freq = 0 # Pause
    
    whole_dur = 1/bpm*60*4
    dur       = 0
    for ll in ls: dur += LENGTHS[ll]*whole_dur
    
    return (freq, dur)
    
def play(uc, pin, sequence, bpm, node_length):
    MIN_BPM =  10
    MAX_BPM = 300

    if bpm > MAX_BPM or bpm < MIN_BPM:      raise Exception(f"Geschwindigkeit muss zwischen {MIN_BPM} und {MAX_BPM} liegen")
    if node_length > 1 or node_length <= 0: raise Exception(f"Notenlaenge muss > 0 und kleiner 1 betragen")

    sequence = sequence.lower()
    seq      = []
    for i,note in enumerate(sequence.split(",")):
        try: seq.append(convert_note(note.strip(), bpm))
        except Exception as ex: raise Exception(f"Ungueltiges Notenformat '{note}' an Stelle {i}: {ex}")
            
    for freq, dur in seq:
        dur_on  = dur * node_length
        dur_off = dur - dur_on
        
        uc.playFrequency(pin, freq)
        time.sleep(dur_on)
        uc.playFrequency(pin, 0)
        time.sleep(dur_off)