import pygame
import constants
import settings
from states.basestate import BaseState

from components.option import *

class OptionsPreferenceState(BaseState):
    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super(OptionsPreferenceState, self).__init__()

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        #Call a function when you press enter.
        self.options = []
        option_index = 0
        for option_name, option_value in settings.settings['preferences'].items():
            if option_value == None:
                option = Option(option_name, option_index, option_value, x = 21, option_font = 'regular')

            elif isinstance(option_value, bool):
                option = CheckboxOption(option_name, option_index, option_value)
            else:
                option = NumberOption(option_name, option_index, option_value)

            option.alphabet.y = 207 + (option.i * 119)

            #print(option_name)
            self.options.append(option)
            option_index += 1

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

        def do_increment():
            self.cur_pick += increment
            #lower limit
            if self.cur_pick < 0:
                self.cur_pick = len(self.options) - 1
            #upper limit
            if self.cur_pick > len(self.options) - 1:
                self.cur_pick = 0
        
        do_increment()
        while self.options[self.cur_pick].value == None:
            do_increment()
        
    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            #Exit menu
            if event.key in settings.settings['keybinds']['back']:
                if self.is_flashing:
                    cancel_sound = pygame.mixer.Sound('assets/sounds/cancelMenu.ogg')
                    cancel_sound.set_volume(settings.settings['volume'] / 10)
                    cancel_sound.play()

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
            for option in self.options:
                option.handle_event(event, self)

    def tick(self, dt):
        for option in self.options:
            i = option.i - self.cur_pick

            #lerp y to the selection position
            option.alphabet.y += ((207 + (i * 119)) - option.alphabet.y) * (dt * 3)
            #cap y position. This took me SO LONG
            option.alphabet.y = min(option.alphabet.y, 107 + (option.i * 119))

            option.tick(dt, self)

        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                self.options[self.cur_pick].toggle()

                settings.write_settings(settings.settings)

                self.is_flashing = False
                self.flash_time = 0

    def draw(self, screen):
        screen.blit(self.bg_image, self.bg_image.get_rect(center = constants.SCREEN_CENTER))

        for option in self.options: 
            #Make the selection the only one with full transparency.
            for character in option.alphabet.character_list:
                if option.value == None: continue

                cur_char_frame = character.animation.getCurrentFrame()

                cur_char_frame.set_alpha(128)
                if self.cur_pick == option.i:
                    cur_char_frame.set_alpha(0)

                    if self.flash_time % (self.flash_speed / 2) <= self.flash_speed / 4:
                        cur_char_frame.set_alpha(255)

            option.draw(screen)