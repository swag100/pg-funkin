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

    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        
        if 'song offset' in self.persistent_data:
            self.conductor.offset = self.persistent_data['song offset']
            
    def handle_event(self, event): 
        pass

    def tick(self, dt): 
        self.conductor.tick(dt)

        pygame.mixer.music.set_volume(settings['volume'] / 30)

    def draw(self, screen): 
        pass