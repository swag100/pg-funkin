import pygame
import constants
from .basestate import BaseState

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.

class MainMenuState(BaseState):
    def __init__(self):
        super(MainMenuState, self).__init__()
        
        print('Im in the main menu!!')

        self.options = [
            'StoryMenuState',
            'OptionsMenuState',
            'CreditsMenuState'
        ]

        self.cur_pick = 1 #The Id of the menu option you're selecting.

        #VISUALS
        self.bg_image = pygame.image.load('assets/images/menuBG.png').convert()
        self.bg_image_magenta = pygame.image.load('assets/images/menuBGMagenta.png').convert()

        self.bg_image = pygame.transform.smoothscale_by(self.bg_image, 1.5)
        self.bg_image_magenta = pygame.transform.smoothscale_by(self.bg_image_magenta, 1.5)

        self.bg_rect = self.bg_image.get_rect(center = constants.SCREEN_CENTER)
    
    def increment_pick(self, increment):
        self.cur_pick += increment
        #lower limit
        if self.cur_pick < 1:
            self.cur_pick = len(self.options)
        #upper limit
        if self.cur_pick > len(self.options):
            self.cur_pick = 1

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            #Advancing in the menu
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                self.increment_pick(-1)
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                self.increment_pick(1)
            
            #entering the picked option
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                self.next_state = self.options[self.cur_pick - 1]
                self.done = True

    def tick(self, dt):
        self.bg_rect.centery += (-(self.cur_pick * 100) - self.bg_rect.centery + (self.bg_rect.h / 2)) * (dt * 2)
        print(self.cur_pick, self.options[self.cur_pick - 1])

    def draw(self, screen):
        screen.blit(self.bg_image, self.bg_rect)