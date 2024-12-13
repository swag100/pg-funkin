import pygame

class BaseState(object):
    def __init__(self):
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persistent_data = {}
        self.next_state = None
        self.done = False
    def start(self, persistent_data): self.persistent_data = persistent_data
    def handle_event(self, event): pass
    def tick(self, dt): pass
    def draw(self, screen): pass