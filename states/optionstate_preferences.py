import pygame
import constants
import settings
from states.basestate import BaseState

from components.spritesheet import Spritesheet
from components.alphabet import Alphabet

class Option:
    def __init__(self, text, i, position = [120, 0]):
        self.text = text
        self.alphabet = Alphabet(text, position)
        self.position = position
        self.i = i

        self.activate_keys = settings.settings['keybinds']['forward']

        self.alphabet.y = 207 + (i * 120)

    def handle_event(self, event):
        pass

    def tick(self, dt, i):
        self.alphabet.x = self.position[0]

        #lerp y to the selection position
        self.alphabet.y += ((207 + (i * 119)) - self.alphabet.y) * (dt * 2.5)

        #cap y position. This took me SO LONG
        self.alphabet.y = min(self.alphabet.y, 107 + (self.i * 120))

        self.alphabet.tick(dt)

class CheckboxOption(Option): #An option with a checkmark.
    def __init__(self, text, i, start_value, position = [120, 0]):
        Option.__init__(self, text, i, position)
        self.value = start_value

        sheet = Spritesheet('assets/images/ui/checkboxThingie.png', 0.71)
        sheet.preload_animations()
        self.animations = sheet.animations

        self.offsets = { #Bottom of sprite is aligned with text, so only x offset is needed.
            'Check Box unselected': (21, 0),
            'Check Box Selected Static': (12, -36),
            'Check Box selecting animation': (6, -22)
        }

        if start_value:
            self.play_anim('Check Box Selected Static')
        else:
            self.play_anim('Check Box unselected')

    def play_anim(self, prefix):
        self.anim_prefix = prefix
        if self.anim_prefix in self.animations:
            self.animation = self.animations[self.anim_prefix]
            self.animation.play()
    
    def toggle(self):
        if self.value:
            self.play_anim('Check Box unselected')
        else:
            self.play_anim('Check Box selecting animation')

        self.value = not self.value
        settings.settings['preferences'][self.text] = self.value

class NumberOption(Option): #An option that is a number, can be any type.
    def __init__(self, text, i, start_value, position = [120, 0]):
        Option.__init__(self, text, i, position)
        self.value = start_value

        self.activate_keys = settings.settings['keybinds']['menu_left'] + settings.settings['keybinds']['menu_right']

        self.value_text = Alphabet(str(start_value), [10, self.alphabet.y], font = 'regular')
        #print(self.value_text.x, self.value_text.y)
    
    def handle_event(self, event):
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            holding_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

            if event.key in settings.settings['keybinds']['menu_left']:
                self.value -= 10 if holding_shift else 1
            if event.key in settings.settings['keybinds']['menu_right']:
                self.value += 10 if holding_shift else 1

            print(self.alphabet.text, self.value)

        self.value_text.text = str(self.value)

        settings.settings['preferences'][self.alphabet.text] = self.value
        settings.write_settings(settings.settings)

class OptionsPreferenceState(BaseState):
    def start(self, persistent_data): 
        self.persistent_data = persistent_data
        super(OptionsPreferenceState, self).__init__()

        self.cur_pick = 0 #The Id of the menu option you're selecting.

        #Call a function when you press enter.
        self.options = []
        option_index = 0
        for option_name, option_value in settings.settings['preferences'].items():
            if isinstance(option_value, bool):
                option = CheckboxOption(option_name, option_index, option_value)
            else:
                option = NumberOption(option_name, option_index, option_value)

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
            for option in self.options:
                if option.i == self.cur_pick and event.key in option.activate_keys:
                    if isinstance(option, CheckboxOption):
                        confirm_sound = pygame.mixer.Sound('assets/sounds/confirmMenu.ogg')
                        confirm_sound.set_volume(settings.settings['volume'] / 10)
                        confirm_sound.play()

                        self.is_flashing = True

                    if isinstance(option, NumberOption):
                        option.handle_event(event)

    def tick(self, dt):
        for option in self.options:
            option.position[0] = 120
            if option.i == self.cur_pick:
                option.position[0] += 30

            if isinstance(option, CheckboxOption):
                option.animation.tickFrameNum()

            if isinstance(option, NumberOption):
                option.value_text.tick(dt)

            option.tick(dt, option.i - self.cur_pick)

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
                cur_char_frame = character.animation.getCurrentFrame()

                cur_char_frame.set_alpha(128)
                if self.cur_pick == option.i:
                    cur_char_frame.set_alpha(0)

                    if self.flash_time % (self.flash_speed / 2) <= self.flash_speed / 4:
                        cur_char_frame.set_alpha(255)

            if isinstance(option, CheckboxOption):
                position = option.animation.getCurrentFrame().get_rect(
                    left = option.offsets[option.anim_prefix][0], 
                    bottom = option.alphabet.y - option.offsets[option.anim_prefix][1]
                )

                option.animation.blit(screen, position)

            if isinstance(option, NumberOption):
                option.value_text.draw(screen)

            option.alphabet.draw(screen)