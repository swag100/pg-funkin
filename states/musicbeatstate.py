import pygame
from settings import settings
from .basestate import BaseState

from components.conductor import Conductor

class MusicBeatState(BaseState):
    def __init__(self):
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.next_state = None
        self.done = False


    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        
        self.conductor = Conductor(102)
        
        #if im not playing already
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load('assets/music/freakyMenu.ogg')

            pygame.mixer.music.set_volume(settings['volume'] / 30)
            
            #this WILL be put in titleState eventually... 
            pygame.mixer.music.play()
            
    def handle_event(self, event): 
        pass

    def tick(self, dt): 
        self.conductor.tick(dt)

        pygame.mixer.music.set_volume(settings['volume'] / 30)

    def draw(self, screen): 
        pass