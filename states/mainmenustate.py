import pygame
import constants
import settings
from .basestate import BaseState

from components.spritesheet import Spritesheet

class MenuOptionSprite:
    def __init__(self, id, state_name):
        self.id = id
        self.state_name = state_name

        self.spritesheet = Spritesheet(f'assets/images/mainmenu/{state_name}.png')
        self.spritesheet.preload_animations()

    def tick(self, cur_pick):
        self.selected = cur_pick == self.id

        self.anim_name = f'{self.state_name} idle'
        if self.selected:
            self.anim_name = f'{self.state_name} selected'

        self.animation = self.spritesheet.animations[self.anim_name]
        self.animation.play()

        self.rect = self.animation.getRect()

        self.rect.centerx = constants.SCREEN_CENTER[0]
        self.rect.y = (self.id * 165) + 52
        if self.selected:
            self.rect.y -= 16

        self.animation.tickFrameNum()

    def draw(self, screen):
        self.animation.blit(screen, self.rect)


class MainMenuState(BaseState):
    def start(self, persistent_data):
        self.persistent_data = persistent_data

        super(MainMenuState, self).__init__()
        
        #print('Im in the main menu!!')

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

        self.is_flashing = False
        self.flash_time = 0 #How long have we been flashing?

        self.max_flash_time = 1 #How long should the flashing last?
        self.flash_speed = (1 / 4)

        #VISUALS
        self.bg_image = pygame.image.load('assets/images/menuBG.png').convert()
        self.bg_image_magenta = pygame.image.load('assets/images/menuBGMagenta.png').convert()

        self.bg_image = pygame.transform.smoothscale_by(self.bg_image, 1.5)
        self.bg_image_magenta = pygame.transform.smoothscale_by(self.bg_image_magenta, 1.5)

        self.bg_rect = self.bg_image.get_rect(center = constants.SCREEN_CENTER)
        self.bg_y_float = self.bg_rect.y #Just so that it looks smooth

        self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
        self.scroll_sound.set_volume(settings.settings['volume'] / 10)
    
    def increment_pick(self, increment):
        self.scroll_sound.set_volume(settings.settings['volume'] / 10)
        self.scroll_sound.play()

        self.cur_pick += increment
        #lower limit
        if self.cur_pick < 0:
            self.cur_pick = len(self.options) - 1
        #upper limit
        if self.cur_pick > len(self.options) - 1:
            self.cur_pick = 0

    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            if self.is_flashing: 
                if event.key in settings.settings['keybinds']['back']:
                    cancel_sound = pygame.mixer.Sound('assets/sounds/cancelMenu.ogg')
                    cancel_sound.set_volume(settings.settings['volume'] / 10)
                    cancel_sound.play()

                    self.is_flashing = False
                    self.flash_time = 0
                return

            #Advancing in the menu
            if event.key in settings.settings['keybinds']['menu_up']:
                self.increment_pick(-1)
            if event.key in settings.settings['keybinds']['menu_down']:
                self.increment_pick(1)
            
            #entering the picked option
            if event.key in settings.settings['keybinds']['forward']:
                confirm_sound = pygame.mixer.Sound('assets/sounds/confirmMenu.ogg')
                confirm_sound.set_volume(settings.settings['volume'] / 10)
                confirm_sound.play()

                self.is_flashing = True

    def tick(self, dt):
        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                self.next_state = self.options[self.cur_pick]
                self.done = True

        self.bg_y_float += (-(self.cur_pick * 100) - self.bg_y_float) * dt

        for menu_option in self.menu_option_sprites: menu_option.tick(self.cur_pick)

    def draw(self, screen):
        screen.blit(self.bg_image, (self.bg_rect.x, self.bg_y_float))
        if self.is_flashing:
            if self.flash_time % self.flash_speed <= self.flash_speed / 2:
                screen.blit(self.bg_image_magenta, (self.bg_rect.x, self.bg_y_float))

            for menu_option in self.menu_option_sprites: 
                if menu_option.selected:
                    if self.flash_time % (self.flash_speed / 2) <= self.flash_speed / 4: 
                        menu_option.draw(screen)
                else:
                    menu_option.draw(screen)
             
        else:
            for menu_option in self.menu_option_sprites: 
                menu_option.draw(screen)