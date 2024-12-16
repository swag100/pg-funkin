import pygame
import settings
from .basestate import BaseState

from components.song import Song
from components.strumline import Strumline

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        self.song = Song('bopeebo')

        #create strums
        opponent_strumline = Strumline((16, 24), True)
        player_strumline = Strumline((700 -24, 24), False)
        self.strumlines = [opponent_strumline, player_strumline]
        
        #song object
        self.song.start()
        
    def handle_event(self, event): 
        for strumline in self.strumlines: strumline.handle_event(event)

        if event == pygame.event.Event(settings.BEAT_HIT): #BEAT HIT
            # print("Beat hit",self.conductor.cur_beat)

            #metronome
            high_beep = pygame.mixer.Sound("assets/sounds/metronome1.ogg")
            high_beep.set_volume(settings.volume)
            low_beep = pygame.mixer.Sound("assets/sounds/metronome2.ogg")
            low_beep.set_volume(settings.volume)
            if self.song.conductor.cur_beat > -1: 
                if self.song.conductor.cur_beat % 4 == 0:
                    high_beep.play()
                else:
                    low_beep.play()

    def tick(self, dt):
        self.song.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for strumline in self.strumlines: strumline.draw(screen)