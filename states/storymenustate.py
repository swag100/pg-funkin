import pygame
import constants
import json
import os
from .basestate import BaseState

from components.spritesheet import Spritesheet

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.
    
def increment_selection(var, li, increment):
    var += increment
    #lower limit
    if var < 0: var = len(li) - 1
    #upper limit
    if var > len(li) - 1: var = 0
    return var

class DifficultyImage:
    def __init__(self, pos, difficulty_name):
        self.difficulty_images = {}
        for file in os.scandir('assets/images/storymenu/difficulties/'):
            if file.is_file():
                self.difficulty_images[file.name.split('.')[0]] = pygame.image.load(f'assets/images/storymenu/difficulties/' + file.name).convert_alpha()

        self.image = self.difficulty_images[difficulty_name]
        self.rect = self.image.get_rect(center = pos)

    def update_image(self, difficulty_name):
        self.image = self.difficulty_images[difficulty_name]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ArrowSelector:
    def __init__(self, pos, is_left = False):
        self.pos = pos
        self.direction = 'left' if is_left else 'right'

        spritesheet = Spritesheet('assets/images/storymenu/ui/arrows.png')
        spritesheet.preload_animations()
        self.animations = spritesheet.animations

        self.animation = self.animations[self.direction + 'Idle']
        self.animation.play()

        #leftIdle, rightIdle, leftConfirm, rightConfirm

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_' + self.direction]:
                self.animation = self.animations[self.direction + 'Confirm']
                self.animation.play()
        if event.type == pygame.KEYUP:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_' + self.direction]:
                self.animation = self.animations[self.direction + 'Idle']
                self.animation.play()
                
    def draw(self, screen):
        self.animation.blit(screen, self.pos)

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
        for level_data in self.level_data_dict.values():
            self.week_options.append(WeekOption(i, level_data['titleAsset']))
            i += 1
        self.week_option_selection = 0

        #Populate difficulty options list
        self.difficulty_options = ['easy', 'normal', 'hard']
        self.difficulty_option_selection = 1 #Start on normal.

        self.font = pygame.font.Font('assets/fonts/vcr.ttf', 32)
        self.track_text_pos = (136, 500)
        self.track_text = self.font.render('TRACKS', True, (229, 87, 119))

        self.prop_bg = pygame.Rect(0, 56, 1280, 400)

        #Difficulty selector
        self.difficulty_selector_objects = [
            ArrowSelector((870,480), True),
            ArrowSelector((1245,480))
        ]

    def find_track_list(self, level_name): #Find a track list for a given level name.
        return self.level_data_dict[level_name]['songs']

    def set_volume_and_play(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
        sound.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up'] + constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                self.set_volume_and_play('assets/sounds/scrollMenu.ogg')

                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                    self.week_option_selection = increment_selection(self.week_option_selection, self.week_options, -1)
                else:
                    self.week_option_selection = increment_selection(self.week_option_selection, self.week_options, 1)

            #Select difficulty
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_left'] + constants.SETTINGS_DEFAULT_KEYBINDS['menu_right']:
                self.set_volume_and_play('assets/sounds/scrollMenu.ogg')

                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_left']:
                    self.difficulty_option_selection = increment_selection(self.difficulty_option_selection, self.difficulty_options, -1)
                else:
                    self.difficulty_option_selection = increment_selection(self.difficulty_option_selection, self.difficulty_options, 1)

            #Exit menu
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['back']:
                self.set_volume_and_play('assets/sounds/cancelMenu.ogg')

                self.next_state = 'MainMenuState' #Go back! Also start our sweet little cancel menu sound.
                self.done = True

            #Enter level
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                week = self.week_options[self.week_option_selection].name
                difficulty = self.difficulty_options[self.difficulty_option_selection]

                self.level_data = self.load_level_data(f'assets/data/levels/{week}.json') #I'm WORKING ON IT. And by it, I mean the GUI
                self.level_songs = self.level_data['songs']

                self.persistent_data['songs'] = self.level_songs
                self.persistent_data['difficulty'] = difficulty #Wow, this is variable!
                
                self.next_state = 'PlayState' #Load playstate, make sure to give it the persistant data of the week.
                self.done = True

        for object in self.difficulty_selector_objects: object.handle_event(event)

    def tick(self, dt):
        for option in self.week_options: option.tick(dt, self.week_option_selection)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for option in self.week_options: 
            #Make the selection the only one with full transparency.
            option.image.set_alpha(128)

            if self.week_option_selection == option.id:
                option.image.set_alpha(255)

            if option.y >= self.prop_bg.y:
                option.draw(screen)

        pygame.draw.rect(screen, (249,207,81), self.prop_bg) #Drawn before characters, but after week options!

        #Draw TRACKS text, + the week's tracklist
        screen.blit(self.track_text, self.track_text_pos)
        track_list = self.find_track_list(self.week_options[self.week_option_selection].name)
        for track_name in track_list:
            formatted_track_string = track_name.replace('-', ' ').title()

            track_text = self.font.render(formatted_track_string, True, (229, 87, 119))
            track_pos = (
                self.track_text_pos[0] - (track_text.get_rect().w / 2) + (self.track_text.get_rect().w / 2),
                self.track_text_pos[1] + (32 * track_list.index(track_name)) + 64
            )
            screen.blit(track_text, track_pos)

        for object in self.difficulty_selector_objects: object.draw(screen)