import sys
import pygame
import constants
import settings
from states.basestate import BaseState

from components.alphabet import Alphabet
from components.option import *

KEYBIND_MENU_NAMES = {
    'menu_left': 'left',
    'menu_down': 'down',
    'menu_up': 'up',
    'menu_right': 'right',

    'forward': 'accept',

    'volume_up': 'up',
    'volume_down': 'down',
    'volume_mute': 'mute'
}

class OptionsKeyBindState(BaseState):
    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super(OptionsKeyBindState, self).__init__()

        self.cur_pick = 1 #The Id of the menu option you're selecting.
        self.cur_keybind = 0 #Can be either 0 or 1, the item in the keybind you are trying to edit.

        self.upper_bound = 177 #Height of selection the screen should go up.
        self.lower_bound = 627 #Height of selection the screen should go down.

        #Call a function when you press enter.
        self.options = []
        option_index = 0
        for option_name, option_value in settings.settings['keybinds'].items():
            visual_text = KEYBIND_MENU_NAMES[option_name] if option_name in KEYBIND_MENU_NAMES else option_name

            if option_value == None:
                option = Option(option_name, option_index, option_value, centered = True)

            else:
                option = KeyBindOption(option_name, option_index, option_value, visual_text)

            option.alphabet.y = 107 + (option.i * 70)

            #print(option_name)
            self.options.append(option)
            option_index += 1

        #VISUALS
        self.bg_image = pygame.transform.smoothscale_by(pygame.image.load('assets/images/menuDesat.png').convert(), 1.1)

        #audio
        self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
        self.set_volume_and_play()
    
    def set_volume_and_play(self):
        self.scroll_sound.set_volume(settings.settings['volume'] / 10)
        self.scroll_sound.play()

    def increment_pick(self, increment):
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
    
    def get_keybind(self):
        banned_keys = [pygame.K_BACKSPACE]
        key = None

        release_times = 0

        game = self.persistent_data['game']
        text_objects = [
            Alphabet('press any key to rebind', [110, 254]),
            Alphabet('backspace to unbind', [110, 485]),
            Alphabet('escape to cancel', [270, 561])
        ]
        done = False
        while not done:

            dt = game.clock.tick(settings.settings['preferences']['fps']) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                
                if event.type == pygame.KEYUP:
                    if release_times == 0:
                        release_times += 1
                    else:
                        key = event.key
                        if key in banned_keys:
                            key = None

                        done = True
            if game.focused:
                self.tick(dt)

                for text in text_objects: text.tick(dt)

                self.draw(game.screen)

                cover = pygame.Surface(constants.WINDOW_SIZE, pygame.SRCALPHA)
                cover.fill((0,0,0,255 * 0.5))
                game.screen.blit(cover, (0,0))

                overlay = pygame.Rect(100, 100, constants.WINDOW_SIZE[0] - 200, constants.WINDOW_SIZE[1] - 200)
                pygame.draw.rect(game.screen, (250,253,109), overlay)

                for text in text_objects: text.draw(game.screen)

            pygame.display.flip()

        return key
        
    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            #Exit menu
            if event.key in settings.settings['keybinds']['back']:
                self.next_state = 'OptionsMenuState' #Go back! Also start our sweet little cancel menu sound.
                self.done = True

            if event.key in settings.settings['keybinds']['menu_up']:
                self.set_volume_and_play()
                self.increment_pick(-1)
            if event.key in settings.settings['keybinds']['menu_down']:
                self.set_volume_and_play()
                self.increment_pick(1)

            if self.cur_keybind == 1:
                if event.key in settings.settings['keybinds']['menu_left']:
                    self.set_volume_and_play()
                    self.cur_keybind = 0
            else:
                if event.key in settings.settings['keybinds']['menu_right']:
                    self.set_volume_and_play()
                    self.cur_keybind = 1
            
            #entering the picked option
            for option in self.options:
                option.handle_event(event, self)

    def tick(self, dt):
        for option in self.options:
            option.tick(dt, self)

            i = option.i - self.cur_pick

            if self.options[self.cur_pick].alphabet.y > self.lower_bound:
                #lerp y to the selection position
                option.alphabet.y += ((self.lower_bound + (i * 70)) - option.alphabet.y) * (dt * 3)

            elif self.options[self.cur_pick].alphabet.y < self.upper_bound:
                #lerp y to the selection position
                option.alphabet.y += ((self.upper_bound + (i * 70)) - option.alphabet.y) * (dt * 3)

    def draw(self, screen):
        self.screen = screen

        screen.blit(self.bg_image, self.bg_image.get_rect(center = constants.SCREEN_CENTER))

        for option in self.options: 
            #Make the selection the only one with full transparency.
            for character in option.alphabet.character_list:
                if option.value == None: continue

                cur_char_frame = character.animation.getCurrentFrame()

                cur_char_frame.set_alpha(128)
                if self.cur_pick == option.i:
                    cur_char_frame.set_alpha(255)

            if hasattr(option, 'keybind_text_list'):
                for key in option.keybind_text_list:
                    for character in key.character_list:
                        if option.value == None: continue

                        cur_char_frame = character.animation.getCurrentFrame()

                        cur_char_frame.set_alpha(128)
                        if self.cur_pick == option.i and self.cur_keybind == option.keybind_text_list.index(key):
                            cur_char_frame.set_alpha(255)

            option.draw(screen)