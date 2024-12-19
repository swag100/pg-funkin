import pygame
import settings
import random
import os
from .basestate import BaseState

from components.song import Song
from components.strumline import Strumline
from components.popup import Popup

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        #chart reader object
        self.song = Song('bopeebo', 'hard')

        #popup sprite group
        self.popups = []

        #create strums
        self.strums = []
        for i in range(8):
            self.strums.append(Strumline(i, self.song))

        self.song.start()
        
    def handle_event(self, event): 
        for strumline in self.strums: strumline.handle_event(event)

        if event.type == pygame.USEREVENT:
            if event.id in settings.HIT_WINDOWS.keys():
                rating = Popup(event.id, (500, 500))
                #Create rating object, add rating to song.ratings list, award score
                self.popups.append(rating)

            if event.id == 'miss':
                miss_noise_path = os.path.join('assets', 'sounds', 'gameplay', f'missnote{random.randint(1, 2)}.ogg')
                miss_noise = pygame.mixer.Sound(miss_noise_path)
                miss_noise.set_volume(settings.volume * 0.5)
                miss_noise.play()

            """
            if event.id == settings.BEAT_HIT: #BEAT HIT
                high_beep = pygame.mixer.Sound("assets/sounds/metronome1.ogg")
                high_beep.set_volume(settings.volume)
                low_beep = pygame.mixer.Sound("assets/sounds/metronome2.ogg")
                low_beep.set_volume(settings.volume)
                if self.song.conductor.cur_beat >= 0: 
                    if self.song.conductor.cur_beat % 4 == 0:
                        high_beep.play()
                    else:
                        low_beep.play()
            """

    def tick(self, dt):
        self.song.conductor.tick(dt)

        for strumline in self.strums: strumline.tick(dt)
        for popup in self.popups: popup.tick(dt)

        #for note in self.song.chart_reader.chart: note.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for strumline in self.strums: strumline.draw(screen)
        for popup in self.popups: popup.draw(screen)
        
        #for note in self.song.chart_reader.chart: note.draw(screen)