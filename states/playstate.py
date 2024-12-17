import pygame
import settings
from .basestate import BaseState

from components.song import Song
from components.strumline import Strumline

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        #chart reader object
        self.song = Song('bopeebo', 'hard')

        #create strums
        self.strums = []
        for i in range(8):
            self.strums.append(Strumline(i, self.song.chart_reader))

        self.song.start()
        
    def handle_event(self, event): 
        for strumline in self.strums: strumline.handle_event(event)

        if event.type == pygame.USEREVENT:
            if event.id == settings.BEAT_HIT: #BEAT HIT

                #metronome
                #print("Beat hit",self.song.conductor.cur_beat)
                high_beep = pygame.mixer.Sound("assets/sounds/metronome1.ogg")
                high_beep.set_volume(settings.volume)
                low_beep = pygame.mixer.Sound("assets/sounds/metronome2.ogg")
                low_beep.set_volume(settings.volume)
                if self.song.conductor.cur_beat >= 0: 
                    if self.song.conductor.cur_beat % 4 == 0:
                        high_beep.play()
                    else:
                        low_beep.play()

    def tick(self, dt):
        self.song.conductor.tick(dt)
        for strum in self.strums: strum.tick(dt)

        #for note in self.song.chart_reader.chart: note.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for strumline in self.strums: strumline.draw(screen)
        #for note in self.song.chart_reader.chart: note.draw(screen)