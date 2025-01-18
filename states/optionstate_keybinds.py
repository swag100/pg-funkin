import pygame
import constants
import settings
from states.basestate import BaseState

from components.alphabet import Alphabet

class Option:
    def __init__(self, text, position = [200, 0]):
        self.text = text
        self.alphabet = Alphabet(text, position)
        self.position = position

    def tick(self, dt, i):
        #lerp them to the selection position
        self.alphabet.x += ((self.position[0]) - self.alphabet.x) * (dt * 3)
        self.alphabet.y += ((constants.SCREEN_CENTER[1] + (i * 150)) - self.alphabet.y) * (dt * 3)

        self.alphabet.tick(dt)

    def handle_event(self, event):
        pass

class OptionsKeyBindState(BaseState):
    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super(OptionsKeyBindState, self).__init__()

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        #Call a function when you press enter.
        self.options = [
            Option('offset'),
            Option('offset'),
            Option('offset'),
        ]

        #Flashing variables.
        self.is_flashing = False
        self.flash_time = 0 #How long have we been flashing?

        self.max_flash_time = 1 #How long should the flashing last?
        self.flash_speed = (1 / 4)

        #VISUALS
        self.bg_image = pygame.transform.smoothscale_by(pygame.image.load('assets/images/menuDesat.png').convert(), 1.1)

        #audio
        self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
        self.scroll_sound.set_volume(settings.settings['volume'] / 10)
        self.scroll_sound.play()
    
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
            #Exit menu
            if event.key in settings.settings['keybinds']['back']:
                if self.is_flashing:
                    #Cancel picking an option!
                    self.is_flashing = False
                    self.flash_time = 0
                else:
                    self.next_state = 'OptionsMenuState' #Go back! Also start our sweet little cancel menu sound.
                    self.done = True

            #Advancing in the menu
            if self.is_flashing: return

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
        for option in self.options: 
            option.tick(dt, self.options.index(option) - self.cur_pick)

        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                print(self.options[self.cur_pick]) #self.options[self.cur_pick]()

                self.is_flashing = False
                self.flash_time = 0

    def draw(self, screen):
        screen.blit(self.bg_image, self.bg_image.get_rect(center = constants.SCREEN_CENTER))

        for option in self.options: 
            #Make the selection the only one with full transparency.
            for character in option.alphabet.character_list:
                character.animation.getCurrentFrame().set_alpha(128)

                if self.cur_pick == self.options.index(option):
                    character.animation.getCurrentFrame().set_alpha(255)

            option.alphabet.draw(screen)
        #if self.is_flashing: #work on this later