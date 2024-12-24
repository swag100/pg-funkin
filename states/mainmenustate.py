import pygame
import constants
from .basestate import BaseState

from components.spritesheet import Spritesheet

class MenuOptionSprite:
    def __init__(self, id, state_name):
        self.id = id
        self.state_name = state_name

        self.spritesheet = Spritesheet(f'assets/images/mainmenu/{state_name}.png')
        self.spritesheet.preload_animations()

    def tick(self, cur_pick):
        self.anim_name = f'{self.state_name} idle'
        if cur_pick == self.id:
            self.anim_name = f'{self.state_name} selected'

        self.animation = self.spritesheet.animations[self.anim_name]
        self.animation.play()

        self.rect = self.animation.getCurrentFrame().get_rect(centerx = constants.SCREEN_CENTER[0])
        self.rect.y = (self.id * 165) + 32

        self.animation.tickFrameNum()

    def draw(self, screen):
        self.animation.blit(screen, self.rect)


class MainMenuState(BaseState):
    def __init__(self):
        super(MainMenuState, self).__init__()
        
        print('Im in the main menu!!')

        self.options = [
            'StoryMenuState',
            'FreeplayMenuState',
            'OptionsMenuState',
            'CreditsMenuState'
        ]
        
        self.menu_option_sprites = [
            MenuOptionSprite(0, 'storymode'),
            MenuOptionSprite(1, 'freeplay'),
            MenuOptionSprite(2, 'options'),
            MenuOptionSprite(3, 'credits')
        ]

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        #VISUALS
        self.bg_image = pygame.image.load('assets/images/menuBG.png').convert()
        self.bg_image_magenta = pygame.image.load('assets/images/menuBGMagenta.png').convert()

        self.bg_image = pygame.transform.smoothscale_by(self.bg_image, 1.5)
        self.bg_image_magenta = pygame.transform.smoothscale_by(self.bg_image_magenta, 1.5)

        self.bg_rect = self.bg_image.get_rect(center = constants.SCREEN_CENTER)
        self.bg_y_float = self.bg_rect.y #Just so that it looks nice
    
    def increment_pick(self, increment):
        self.cur_pick += increment
        #lower limit
        if self.cur_pick < 0:
            self.cur_pick = len(self.options) - 1
        #upper limit
        if self.cur_pick > len(self.options) - 1:
            self.cur_pick = 0

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            #Advancing in the menu
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                self.increment_pick(-1)
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                self.increment_pick(1)
            
            #entering the picked option
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                self.next_state = self.options[self.cur_pick]
                self.done = True

    def tick(self, dt):
        self.bg_y_float += (-(self.cur_pick * 100) - self.bg_y_float) * dt

        for menu_option in self.menu_option_sprites: menu_option.tick(self.cur_pick)

    def draw(self, screen):
        screen.blit(self.bg_image, (self.bg_rect.x, self.bg_y_float))

        for menu_option in self.menu_option_sprites: menu_option.draw(screen)