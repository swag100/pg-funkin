import pygame
import constants
from .basestate import BaseState

from components.song import Song

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        self.song = Song('bopeebo')

        #create strums
        #

        #song object
        self.song.start()
        
    def handle_event(self, event): 
        if event == pygame.event.Event(constants.BEAT_HIT): #BEAT HIT
            # print("Beat hit",self.conductor.cur_beat)

            if self.song.conductor.cur_beat > -1: 
                if self.song.conductor.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()

    def tick(self, dt):
        self.song.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))