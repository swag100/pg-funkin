import pygame
import constants
import json
import os
from .basestate import BaseState

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.

class WeekOption:
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.name = path.split('/')[len(path.split('/')) - 1]
        self.image = pygame.image.load('assets/images/'+path+'.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.y = 478 + (id * 128)

    def tick(self, dt, selection):
        self.rect.centerx = constants.SCREEN_CENTER[0]

        i = self.id - selection
        self.y += ((478 + (i * 128)) - self.y) * (dt * 7)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.y))

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

        #Populate week options list, USING SELF DOT LEVEL JSONS!
        self.week_options = []
        i = 0
        for level_name, level_data in self.level_data_dict.items():
            self.week_options.append(WeekOption(i, level_data['titleAsset']))
            i += 1
        self.week_option_selection = 0

        self.font = pygame.font.Font('assets/fonts/vcr.ttf', 32)
        self.track_text_pos = (136, 500)

        self.prop_bg = pygame.Rect(0, 56, 1280, 400)

    def find_track_list(self, level_name): #Find a track list for a given level name.
        return self.level_data_dict[level_name]['songs']
    
    def increment_selection(self, increment):
        self.week_option_selection += increment
        #lower limit
        if self.week_option_selection < 0:
            self.week_option_selection = len(self.week_options) - 1
        #upper limit
        if self.week_option_selection > len(self.week_options) - 1:
            self.week_option_selection = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up'] + constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
                scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                scroll_sound.play()

                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                    self.increment_selection(-1)
                else:
                    self.increment_selection(1)

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
        for option in self.week_options: option.tick(dt, self.week_option_selection)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for option in self.week_options: 
            #Make the selection the only one with full transparency.
            option.image.set_alpha(128)

            if self.week_option_selection == option.id:
                option.image.set_alpha(255)

            option.draw(screen)

        pygame.draw.rect(screen, (249,207,81), self.prop_bg) #Drawn before characters, but after week options!

        screen.blit(self.font.render('TRACKS', True, (229, 87, 119)), self.track_text_pos)

        track_list = self.find_track_list(self.week_options[self.week_option_selection].name)
        for track in track_list:
            track_x = self.track_text_pos[0]
            track_y = self.track_text_pos[1] + (32 * track_list.index(track)) + 64
            screen.blit(self.font.render(track.title(), True, (229, 87, 119)), (track_x, track_y))