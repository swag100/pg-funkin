import pygame

from components.spritesheet import Spritesheet
class Strumline:
    def __init__(self, bot_play):
        self.bot_play = bot_play
        
        #for loop, repeat 4 times make each individual strum
        #What is a strum?