import pygame
import constants
from states.basestate import BaseState

class OptionsMenuState(BaseState):
    def __init__(self):
        super(OptionsMenuState, self).__init__()
    def start(self, persistent_data): 
        self.persistent_data = persistent_data

    def handle_event(self, event): 
        pass

    def tick(self, dt): 
        pass

    def draw(self, screen): 
        pass