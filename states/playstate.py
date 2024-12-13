import pygame
from components.spritesheet import Spritesheet
from .basestate import BaseState

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.persistent_data = {}

        self.done = False
        #self.next_state = None

        #Make sprite group instead of just a list to contain game objects
        self.sheet = Spritesheet('assets/images/noteStrumline.png')
        self.press = 'Down'
    def start(self, persistent_data): 
        pass
    def handle_event(self, event): 
        pass
    def tick(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: self.press = 'Right'
        if keys[pygame.K_LEFT]: self.press = 'Left'
        if keys[pygame.K_UP]: self.press = 'Up'
        if keys[pygame.K_DOWN]: self.press = 'Down'

        self.note = self.sheet.load_animation('static'+self.press)[0]

        pygame.time.Clock().tick(60)
    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.note, self.note.get_rect())
