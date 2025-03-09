import pygame
from settings import settings
from .basestate import BaseState

from components.conductor import Conductor

class MusicBeatState(BaseState):
    def __init__(self):
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.next_state = None
        self.done = False

        self.conductor = Conductor(102)
        
        pygame.mixer.music.load('assets/music/freakyMenu.ogg')

        pygame.mixer.music.set_volume(settings['volume'] / 30)

    def start(self, persistent_data): 
        self.persistent_data = persistent_data

        song_position = 0
        if 'song position' in self.persistent_data:
            song_position = self.persistent_data['song position']

        pygame.mixer.music.play(start=song_position)

    def handle_event(self, event): 
        pass

    def tick(self, dt): 
        self.conductor.tick(dt)

        pygame.mixer.music.set_volume(settings['volume'] / 30)

    def draw(self, screen): 
        pass