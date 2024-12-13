import pygame
from components.spritesheet import Spritesheet
from components.conductor import Conductor
from .basestate import BaseState

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.persistent_data = {}

        self.done = False
        #self.next_state = None

        #Make sprite group instead of just a list to contain game objects
        self.sheet = Spritesheet('assets/images/noteStrumline.png')
        self.conductor = Conductor(100, 0)
    def tick(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: press = 'staticRight'
        elif keys[pygame.K_LEFT]: press = 'staticLeft'
        elif keys[pygame.K_UP]: press = 'staticUp'
        elif keys[pygame.K_DOWN]: press = 'staticDown'
        else: press = 'confirmHoldDown'

        self.note = self.sheet.load_animation(press)[0]
        self.note = pygame.transform.smoothscale_by(self.note, 0.7)

        self.conductor.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.note, self.note.get_rect())
