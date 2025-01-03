import pygame
import constants
import json
import os
from .basestate import BaseState

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.

class WeekOption:
    def __init__(self, id, image):
        self.id = id
        self.image = pygame.image.load('assets/images/storymenu/titles/'+image+'.png').convert_alpha()

        self.center = (0, 0)
        self.rect = self.image.get_rect(center = self.center)
    
    def tick(self, dt):
        self.rect.center = constants.SCREEN_CENTER
        self.rect.y += 56
        self.rect.y += self.id * 116

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class StoryMenuState(BaseState):
    def load_level_data(self, level_path):
        with open(level_path) as level_data_file:
            level_data = json.loads(level_data_file.read())
        level_data_file.close()

        return level_data

    def start(self, persistent_data): 
        self.persistent_data = persistent_data

        super(StoryMenuState, self).__init__()

        self.level_data_dict = {}
        for file in os.scandir('assets/data/levels/'):
            if file.is_file():
                self.level_data_dict[file.name.split('.')[0]] = self.load_level_data(file.path)
        
        self.week_options = []

        #Populate week options list, USING SELF DOT LEVEL JSONS!
        i = 0
        for level_name, level_data in self.level_data_dict.items():
            i += 1
            self.week_options.append(WeekOption(i, level_name))

        self.prop_bg = pygame.Rect(0, 56, 1280, 400)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['back']:
                cancel_sound = pygame.mixer.Sound('assets/sounds/cancelMenu.ogg')
                cancel_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                cancel_sound.play()

                self.next_state = 'MainMenuState' #Go back! Also start our sweet little cancel menu sound.
                self.done = True

            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                self.level_data = self.load_level_data('assets/data/levels/week1.json') #TODO: make it so user can pick a level + difficulty. Requires making the GUI
                self.level_songs = self.level_data['songs']

                self.persistent_data['songs'] = self.level_songs
                self.persistent_data['difficulty'] = 'hard' #TODO: Please, make this variable later..
                
                self.next_state = 'PlayState' #Load playstate, make sure to give it the persistant data of the week.
                self.done = True

    def tick(self, dt):
        for option in self.week_options: option.tick(dt)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for option in self.week_options: option.draw(screen)

        pygame.draw.rect(screen, (249,207,81), self.prop_bg) #Drawn before characters, but after week options!