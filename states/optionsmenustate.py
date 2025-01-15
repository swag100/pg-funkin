import pygame
import constants
from states.basestate import BaseState

from components.alphabet import Alphabet

class OptionsMenuState(BaseState):
    def set_offset(self):
        print('I work')

    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super(OptionsMenuState, self).__init__()

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        #parallel list containing their text
        self.option_text = [
            'offset',
            'offset',
            'offset',
        ]
        #Call a function when you press enter.
        self.options = [
            self.set_offset,
            self.set_offset,
            self.set_offset,
        ]

        self.option_sprites = []
        for i in range(len(self.options)):
            self.option_sprites.append(Alphabet(self.option_text[i], [100, 0]))

        #Flashing variables.
        self.is_flashing = False
        self.flash_time = 0 #How long have we been flashing?

        self.max_flash_time = 1 #How long should the flashing last?
        self.flash_speed = (1 / 4)

        #VISUALS
        self.bg_image = pygame.image.load('assets/images/menuDesat.png').convert()

        #audio
        self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
        self.scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
        self.scroll_sound.play()
    
    def increment_pick(self, increment):
        self.scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
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
            #Exit menu
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['back']:
                cancel_sound = pygame.mixer.Sound('assets/sounds/cancelMenu.ogg')
                cancel_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                cancel_sound.play()

                if self.is_flashing:
                    #Cancel picking an option!
                    self.is_flashing = False
                    self.flash_time = 0
                else:
                    self.next_state = 'MainMenuState' #Go back! Also start our sweet little cancel menu sound.
                    self.done = True

            #Advancing in the menu
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                self.increment_pick(-1)
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                self.increment_pick(1)
            
            #entering the picked option
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                confirm_sound = pygame.mixer.Sound('assets/sounds/confirmMenu.ogg')
                confirm_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                confirm_sound.play()

                self.is_flashing = True

    def tick(self, dt):
        for alphabet in self.option_sprites: 
            i = self.option_sprites.index(alphabet) - self.cur_pick

            #lerp them to the selection position
            selection_position = (100, constants.SCREEN_CENTER[1])
            alphabet.x += ((selection_position[0] + (i * 0)) - alphabet.x) * (dt * 3)
            alphabet.y += ((selection_position[1] + (i * 150)) - alphabet.y) * (dt * 3)

            alphabet.tick(dt)

        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                self.options[self.cur_pick]()

                self.is_flashing = False
                self.flash_time = 0

    def draw(self, screen):
        screen.blit(self.bg_image, (0,0))

        for alphabet in self.option_sprites: 
            #Make the selection the only one with full transparency.
            for character in alphabet.character_list:
                character.animation.getCurrentFrame().set_alpha(128)

                if self.cur_pick == self.option_sprites.index(alphabet):
                    character.animation.getCurrentFrame().set_alpha(255)

            alphabet.draw(screen)
        #if self.is_flashing: #work on this later