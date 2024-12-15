import pygame

from components.spritesheet import Spritesheet

#individual receptor
class StrumlineNote:
    def __init__(self):
        self.default_offset = 13 #from og source code
        

#handles the receptors and the notes (with sustains) for a given player.
class Strumline:
    def __init__(self, bot_play):
        self.bot_play = bot_play

        #for loop, repeat 4 times make each individual strum
        #What is a strum?