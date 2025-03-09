import pygame
import constants
import settings
import json
import os
from .musicbeatstate import MusicBeatState

from components.spritesheet import Spritesheet
from components.prop import AnimatedProp

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.
    
def increment_selection(var, li, increment):
    var += increment
    #lower limit
    if var < 0: var = len(li) - 1
    #upper limit
    if var > len(li) - 1: var = 0
    return var

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

class DifficultyImage:
    def __init__(self, pos, difficulty_name):
        self.difficulty_images = {}
        for file in os.scandir('assets/images/storymenu/difficulties/'):
            if file.is_file():
                self.difficulty_images[file.name.split('.')[0]] = pygame.image.load(f'assets/images/storymenu/difficulties/' + file.name).convert_alpha()

        self.pos = pos
        self.update_image(difficulty_name)

        self.y_off = 0
        self.alpha = 255

    def update_image(self, difficulty_name):
        self.y_off = 50
        self.alpha = 0

        self.image = self.difficulty_images[difficulty_name]

    def tick(self, dt):
        self.y_off += (0 - self.y_off) * dt * 25
        self.alpha += (255 - self.alpha) * dt * 25

        self.rect = self.image.get_rect(centerx = self.pos[0], top = self.pos[1] - self.y_off)
        self.image.set_alpha(self.alpha)

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
            if event.key in settings.settings['keybinds']['menu_' + self.direction]:
                self.animation = self.animations[self.direction + 'Confirm']
                self.animation.play()
        if event.type == pygame.KEYUP:
            if event.key in settings.settings['keybinds']['menu_' + self.direction]:
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

class StoryMenuState(MusicBeatState):
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
    
    def __init__(self):
        #This will be used for preloading all the props, so loading them doesn't cause any lag.
        self.level_data_dict = self.get_data_dict()

        self.props = {}
        for level, data in self.level_data_dict.items():
            for prop in data['props']:
                try:
                    self.props[level].append(AnimatedProp(prop))
                except KeyError:
                    self.props[level] = [AnimatedProp(prop)]
            #print(self.props[level])

    def start(self, persistent_data): 
        self.persistent_data = persistent_data

        super().__init__()
        super().start(self.persistent_data)

        self.level_data_dict = self.get_data_dict()

        #Populate week options list, USING SELF DOT LEVEL JSONS!
        self.week_options = []
        i = 0
        for level_data in self.level_data_dict.values():
            self.week_options.append(WeekOption(i, level_data['titleAsset']))
            i += 1
        self.week_option_selection = 0

        #Flash variables
        self.is_flashing = False
        self.flash_time = 0 #How long have we been flashing?

        self.max_flash_time = 1.2 #How long should the flashing last?
        self.flash_speed = (1 / 4)

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

        self.difficulty_image = DifficultyImage((1080,488),self.difficulty_options[self.difficulty_option_selection])

    def find_track_list(self, level_name): #Find a track list for a given level name.
        return self.level_data_dict[level_name]['songs']

    def get_week_name(self):
        return self.week_options[self.week_option_selection].name

    def enter_level(self, week_name):
        difficulty = self.difficulty_options[self.difficulty_option_selection]

        self.level_data = self.load_level_data(f'assets/data/levels/{week_name}.json') #I'm WORKING ON IT. And by it, I mean the GUI
        self.level_songs = self.level_data['songs']

        self.persistent_data['songs'] = self.level_songs
        self.persistent_data['difficulty'] = difficulty #Wow, this is variable!
        
        self.next_state = 'PlayState' #Load playstate, make sure to give it the persistant data of the week.
        self.persistent_data['song position'] = self.conductor.song_position
        self.done = True

    def set_volume_and_play(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(settings.settings['volume'] / 10)
        sound.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            #Exit menu
        
            if self.is_flashing: 
                if event.key in settings.settings['keybinds']['back']:
                    self.set_volume_and_play('assets/sounds/cancelMenu.ogg')
                    self.is_flashing = False
                    self.flash_time = 0

                return
            else:
                if event.key in settings.settings['keybinds']['back']:
                    self.set_volume_and_play('assets/sounds/cancelMenu.ogg')

                    self.next_state = 'MainMenuState' #Go back! Also start our sweet little cancel menu sound.
                    self.persistent_data['song position'] = self.conductor.song_position
                    self.done = True

            if event.key in settings.settings['keybinds']['menu_up'] + settings.settings['keybinds']['menu_down']:
                self.set_volume_and_play('assets/sounds/scrollMenu.ogg')

                if event.key in settings.settings['keybinds']['menu_up']:
                    self.week_option_selection = increment_selection(self.week_option_selection, self.week_options, -1)
                else:
                    self.week_option_selection = increment_selection(self.week_option_selection, self.week_options, 1)

            #Select difficulty
            if event.key in settings.settings['keybinds']['menu_left'] + settings.settings['keybinds']['menu_right']:
                self.set_volume_and_play('assets/sounds/scrollMenu.ogg')

                if event.key in settings.settings['keybinds']['menu_left']:
                    self.difficulty_option_selection = increment_selection(self.difficulty_option_selection, self.difficulty_options, -1)
                else:
                    self.difficulty_option_selection = increment_selection(self.difficulty_option_selection, self.difficulty_options, 1)

                self.difficulty_image.update_image(self.difficulty_options[self.difficulty_option_selection])

            #Enter level
            if event.key in settings.settings['keybinds']['forward']:
                confirm_sound = pygame.mixer.Sound('assets/sounds/confirmMenu.ogg')
                confirm_sound.set_volume(settings.settings['volume'] / 10)
                confirm_sound.play()

                self.is_flashing = True

                pygame.mixer.music.stop()

                for prop_list in self.props.values(): 
                    for prop in prop_list:
                        if 'confirm' in prop.animations:
                            prop.play_animation('confirm')
        

        if event.type == pygame.USEREVENT:
            event_list = event.id.split('/', 1)
            event_type = event_list[0]
            try:
                event_parameters = event_list[1].split('/')
            except IndexError:
                event_parameters = []

            if event_type == constants.BEAT_HIT: #BEAT HIT
                cur_beat = int(event_parameters[0]) #easier to read

                #play prop anims.
                for prop_list in self.props.values(): 
                    for prop in prop_list:
                        if self.is_flashing(): return
                        
                        if 'idle' in prop.animations.keys():
                            prop.play_animation('idle')
                        else:
                            if cur_beat % 2 == 0:
                                prop.play_animation('danceLeft')
                            else:
                                prop.play_animation('danceRight')


        for object in self.difficulty_selector_objects: object.handle_event(event)

    def tick(self, dt):
        super().tick(dt)

        if self.is_flashing:
            self.flash_time += dt

            if self.flash_time >= self.max_flash_time:
                self.enter_level(self.get_week_name())

        for option in self.week_options: option.tick(dt, self.week_option_selection)
        self.difficulty_image.tick(dt)

        for prop_list in self.props.values(): 
            for prop in prop_list:
                prop.tick()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        for option in self.week_options: 
            if option.y >= self.prop_bg.y: #Make sure it's on screen!

                #Make the selection the only one with full transparency.
                option.image.set_alpha(128)
                if self.week_option_selection == option.id:
                    option.image.set_alpha(255)

                    fill(option.image, (255, 255, 255, 255))
                    if self.is_flashing and self.flash_time % (self.flash_speed / 2) <= self.flash_speed / 4:
                        fill(option.image, (0, 255, 255, 255))

                screen.blit(option.image, (option.rect.x, option.y))

        pygame.draw.rect(screen, (249,207,81), self.prop_bg) #Drawn before characters, but after week options!
        #Draw my beloved characters :face_holding_back_tears:
        for prop in self.props[self.get_week_name()]: prop.draw(screen)

        #Draw TRACKS text, + the week's tracklist
        screen.blit(self.track_text, self.track_text_pos)
        track_list = self.find_track_list(self.get_week_name())
        for track_name in track_list:
            formatted_track_string = track_name.replace('-', ' ').title()

            track_text = self.font.render(formatted_track_string, True, (229, 87, 119))
            track_pos = (
                self.track_text_pos[0] - (track_text.get_rect().w / 2) + (self.track_text.get_rect().w / 2),
                self.track_text_pos[1] + (32 * track_list.index(track_name)) + 64
            )
            screen.blit(track_text, track_pos)

        #Flavor text
        flavor_text_string = self.level_data_dict[self.get_week_name()]['name']
        flavor_text = self.font.render(flavor_text_string, True, (187, 187, 187))
        flavor_text_pos = flavor_text.get_rect(topright = (constants.WINDOW_SIZE[0] - 15, 12))
        screen.blit(flavor_text, flavor_text_pos)

        #Difficulty selectors.
        for object in self.difficulty_selector_objects: object.draw(screen)
        self.difficulty_image.draw(screen)