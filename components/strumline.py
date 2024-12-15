import pygame

from components.spritesheet import Spritesheet

#graphic of individual receptor; handles animations
class StrumlineNote:
    def __init__(self, i, direction):
        self.direction = direction

        self.confirm_offset = 13 #from og source code
        

#handles the receptors and the notes (with sustains) for a given player.
class Strumline:
    def __init__(self, bot_play):
        self.bot_play = bot_play#Bool: Will this strumline take in input?

        self.directions = ['left','down','up','right'] #directions in order
        self.strumline_size = 104 #width of single strum
        self.note_spacing = self.strumline_size + 8

        self.initial_offset = -0.275 * self.strumline_size

        for i in range(len(self.directions)):
            StrumlineNote(i, self.directions[i])

        #for loop, repeat 4 times make each individual strum
        #What is a strum?