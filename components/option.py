import pygame
import constants
import settings

from components.spritesheet import Spritesheet
from components.alphabet import Alphabet

class Option:
    def __init__(self, text, i, start_value, x = 0, y = 0, option_font = 'bold', centered = False):
        self.text = text
        self.i = i
        self.alphabet = Alphabet(text, [x, y], font = option_font)

        self.value = start_value

        self.activate_keys = settings.settings['keybinds']['forward']

        if centered:
            self.alphabet.x = constants.SCREEN_CENTER[0] - (self.alphabet.width / 2)

    def handle_event(self, event, state):
        pass

    def tick(self, dt, state):
        self.alphabet.tick(dt)

    def draw(self, screen):
        self.alphabet.draw(screen)

class CheckboxOption(Option): #An option with a checkmark.
    def __init__(self, text, i, start_value):
        super().__init__(text, i, start_value)

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

    def handle_event(self, event, state):
        if event.type != pygame.KEYDOWN: return

        if self.i == state.cur_pick and event.key in self.activate_keys:
            confirm_sound = pygame.mixer.Sound('assets/sounds/confirmMenu.ogg')
            confirm_sound.set_volume(settings.settings['volume'] / 10)
            confirm_sound.play()
            
            state.is_flashing = True

    def tick(self, dt, state):
        self.alphabet.x = 120
        if self.i == state.cur_pick:
            self.alphabet.x += 30

        super().tick(dt, state)

        self.animation.tickFrameNum()

    def draw(self, screen):
        super().draw(screen)
    
        position = self.animation.getCurrentFrame().get_rect(
            left = self.offsets[self.anim_prefix][0], 
            bottom = self.alphabet.y - self.offsets[self.anim_prefix][1]
        )

        self.animation.blit(screen, position)

class NumberOption(Option): #An option that is a number, can be any type.
    def __init__(self, text, i, start_value):
        super().__init__(text, i, start_value)

        self.value = start_value
        self.value_text = self.update_value_text(self.value)

        #keys used to adjust value.
        self.activate_keys = settings.settings['keybinds']['menu_left'] + settings.settings['keybinds']['menu_right']

    def update_value_text(self, value):
        return Alphabet(str(value), [15, 0], font = 'regular')

    def handle_event(self, event, state):
        if event.type != pygame.KEYDOWN: return
        
        if self.i == state.cur_pick and event.key in self.activate_keys:
            if event.key in settings.settings['keybinds']['menu_left']: 
                self.value -= 5
            if event.key in settings.settings['keybinds']['menu_right']: 
                self.value += 5

            self.value_text = self.update_value_text(self.value)

            settings.settings['preferences'][self.alphabet.text] = self.value
            settings.write_settings(settings.settings)

    def tick(self, dt, state):
        self.alphabet.x = self.value_text.width + self.value_text.x + 60

        super().tick(dt, state)

        self.value_text.y = self.alphabet.y - 7
        self.value_text.tick(dt)

    def draw(self, screen):
        super().draw(screen)
        
        self.value_text.draw(screen)

###

class KeyBindOption(Option):
    def __init__(self, text, i, start_value, visual_text):
        super().__init__(visual_text, i, start_value)

        self.text = text

        self.keybinds = start_value #List of keybinds with a length of 2.
        self.keybind_text_list = self.update_keybind_text_list(self.keybinds)

    def update_keybind_text_list(self, keybinds):
        keybind_text_list = []
        for key in keybinds:
            try:
                key_str = pygame.key.name(int(key)).title()
            except:
                key_str = '___'

            keybind_text_list.append(Alphabet(key_str, [15, 0], font = 'regular'))

        return keybind_text_list

    def handle_event(self, event, state):
        if event.type == pygame.KEYDOWN: 
            if self.i == state.cur_pick and event.key in self.activate_keys:
                value = state.get_keybind()

                self.keybinds[state.cur_keybind] = value

                self.keybind_text_list = self.update_keybind_text_list(self.keybinds)

                settings.settings['keybinds'][self.text] = self.keybinds
                settings.write_settings(settings.settings)

    def tick(self, dt, state):
        self.alphabet.x = 100

        super().tick(dt, state)

        for key in self.keybind_text_list:
            if self.keybind_text_list.index(key) == 0:
                key.x = 650
            else:
                key.x = 1050

            key.y = self.alphabet.y - 7

            key.tick(dt)

    def draw(self, screen):
        super().draw(screen)
        
        for key in self.keybind_text_list:
            key.draw(screen)