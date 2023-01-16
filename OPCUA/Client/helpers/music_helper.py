#!/usr/bin/python
import sys, re, time

class MusicHelper(object):

    def __init__(self, piezo):
        self.__piezo = piezo

        self.__NOTES          = { "c":0, "c#":1, "db":1, "d":2, "d#":3, "eb":3, "e":4, "f":5, "f#":6, "gb":6, "g":7, "g#":8, "ab":8, "a":9, "a#":10, "b":10, "h":11 }
        self.__NOTE_LETTERS   = "|".join(re.escape(n) for n in self.__NOTES.keys())

        self.__LENGTHS        = { "g":1, "h":.5, "v":.25, "a":.125, "s": 0.0625, "t": .5/3 }
        self.__LENGTH_LETTERS = "|".join(re.escape(l) for l in self.__LENGTHS.keys())               
        self.__RE_NOTE        = re.compile(fr"^(?:({self.__NOTE_LETTERS})(-?\d):)?((?:{self.__LENGTH_LETTERS})+)$")

    def __convert_note(self, tone, bpm):
        nl,nh,ls  = self.__RE_NOTE.match(tone).groups()
    
        if nl is not None and nh is not None:
            note_nr   = self.__NOTES[nl] - 8 + int(nh) * 12
            freq      = 440 * (2 ** (1/12)) ** (note_nr - 49)
        else: freq = 0 # Pause
    
        whole_dur = 1/bpm*60*4
        dur       = 0
        for ll in ls: dur += self.__LENGTHS[ll]*whole_dur
    
        return (freq, dur)
    
    def play(self, sequence, bpm=180, node_length=.75):
        MIN_BPM =  10
        MAX_BPM = 300

        if bpm > MAX_BPM or bpm < MIN_BPM:      raise Exception(f"Geschwindigkeit muss zwischen {MIN_BPM} und {MAX_BPM} liegen")
        if node_length > 1 or node_length <= 0: raise Exception(f"Notenlaenge muss > 0 und kleiner 1 betragen")

        sequence = sequence.lower()
        seq      = []
        for i,note in enumerate(sequence.split(",")):
            try: seq.append(self.__convert_note(note.strip(), bpm))
            except Exception as ex: raise Exception(f"Ungueltiges Notenformat '{note}' an Stelle {i}: {ex}")
            
        for freq, dur in seq:
            dur_on  = dur * node_length
        
            self.__piezo.playFrequency(freq, int(dur_on * 1e6))
            time.sleep(dur)