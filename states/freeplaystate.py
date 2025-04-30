import os
import json
import pygame
import constants
import settings
from states.musicbeatstate import MusicBeatState

from components.alphabet import Alphabet

class FreeplayMenuState(MusicBeatState):
    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super().__init__()

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        self.level_data_dict = self.get_data_dict()

        #Call a function when you press enter.
        #122 + (102 * id
        self.options = []

        for level_data in self.level_data_dict.values():
            for song in level_data['songs']:
                self.options.append(Alphabet(song))

        self.selection_position = (100, constants.SCREEN_CENTER[1] + 50)

        #position them immediately!
        for alphabet in self.options: 
            i = self.options.index(alphabet) - self.cur_pick
            alphabet.x += ((self.selection_position[0] + (i * 25)) - alphabet.x)
            alphabet.y += ((self.selection_position[1] + (i * 150)) - alphabet.y)

        #Flashing variables.
        self.is_flashing = False
        self.flash_time = 0 #How long have we been flashing?

        self.max_flash_time = 1 #How long should the flashing last?
        self.flash_speed = (1 / 4)

        #VISUALS
        self.bg_image = pygame.image.load('assets/images/menuBGBlue.png').convert()

        #audio
        self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
        self.scroll_sound.set_volume(settings.settings['volume'] / 10)
        self.scroll_sound.play()

    def load_level_data(self, level_path):
        with open(level_path) as level_data_file:
            level_data = json.loads(level_data_file.read())
        level_data_file.close()

        return level_data
    
    def get_data_dict(self):
        data_dict = {}
        for file in os.scandir('assets/data/levels/'):
            if file.is_file():
                data_dict[file.name.split('.')[0]] = self.load_level_data(file.path)
        return data_dict
    
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
                cancel_sound = pygame.mixer.Sound('assets/sounds/cancelMenu.ogg')
                cancel_sound.set_volume(settings.settings['volume'] / 10)
                cancel_sound.play()

                if self.is_flashing:
                    #Cancel picking an option!
                    self.is_flashing = False
                    self.flash_time = 0
                else:
                    self.next_state = 'MainMenuState' #Go back! Also start our sweet little cancel menu sound.
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
                
                pygame.mixer.music.stop()#make a fade out function later

                self.is_flashing = True

    def tick(self, dt):
        for alphabet in self.options: 
            i = self.options.index(alphabet) - self.cur_pick
            alphabet.x += ((self.selection_position[0] + (i * 25)) - alphabet.x) * (dt * 7)
            alphabet.y += ((self.selection_position[1] + (i * 150)) - alphabet.y) * (dt * 7)
            alphabet.tick(dt)

        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                cur_option_text = self.options[self.cur_pick].text

                self.next_state = 'PlayState'
                self.persistent_data['previous state'] = 'FreeplayMenuState'
                self.persistent_data['songs'] = [cur_option_text]
                self.persistent_data['difficulty'] = 'hard' #CHANGE LATER MAKE VARIABLE

                self.is_flashing = False
                self.flash_time = 0

                self.done = True

    def draw(self, screen):
        screen.blit(self.bg_image, self.bg_image.get_rect(center = constants.SCREEN_CENTER))

        for alphabet in self.options: 
            #Make the selection the only one with full transparency.
            for character in alphabet.character_list:
                cur_char_frame = character.animation.getCurrentFrame()
                cur_char_frame.set_alpha(128)

                if self.cur_pick == self.options.index(alphabet):
                    cur_char_frame.set_alpha(0)

                    if self.flash_time % (self.flash_speed / 2) <= self.flash_speed / 4:
                        cur_char_frame.set_alpha(255)

            alphabet.draw(screen)