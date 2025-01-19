import pygame
import settings

from components.spritesheet import Spritesheet
from components.alphabet import Alphabet

class Option:
    def __init__(self, text, i, start_value, option_font = 'bold'):
        self.text = text
        self.alphabet = Alphabet(text, [21, 0], font = option_font)
        self.i = i

        self.value = start_value

        self.activate_keys = settings.settings['keybinds']['forward']

        self.alphabet.y = 207 + (i * 120)

    def handle_event(self, event, state):
        pass

    def tick(self, dt, state):
        i = self.i - state.cur_pick

        #lerp y to the selection position
        self.alphabet.y += ((207 + (i * 119)) - self.alphabet.y) * (dt * 3)

        #cap y position. This took me SO LONG
        self.alphabet.y = min(self.alphabet.y, 107 + (self.i * 120))

        self.alphabet.tick(dt)

    def draw(self, screen):
        self.alphabet.draw(screen)


class CheckboxOption(Option): #An option with a checkmark.
    def __init__(self, text, i, start_value, x = 0):
        Option.__init__(self, text, i, x)
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
    def __init__(self, text, i, start_value, position = [120, 0]):
        Option.__init__(self, text, i, position)

        self.value = start_value
        self.value_text = self.update_value_text(self.value)

        #keys used to adjust value.
        self.activate_keys = settings.settings['keybinds']['menu_left'] + settings.settings['keybinds']['menu_right']

    def update_value_text(self, value):
        return Alphabet(str(value), [15, 0], font = 'regular')

    def handle_event(self, event, state):
        if event.type != pygame.KEYDOWN: return
        
        if self.i == state.cur_pick and event.key in self.activate_keys:
            keys = pygame.key.get_pressed()

            modifier = any(keys[key] for key in settings.settings['keybinds']['menu_modify'])

            if event.key in settings.settings['keybinds']['menu_left']: self.value -= 1 if modifier else 5
            if event.key in settings.settings['keybinds']['menu_right']: self.value += 1 if modifier else 5

            self.value_text = self.update_value_text(self.value)

            settings.settings['preferences'][self.alphabet.text] = self.value
            settings.write_settings(settings.settings)

    def tick(self, dt, state):
        #Putting this before calling tick on super works??? I don't know why, but okay!
        self.alphabet.x = self.value_text.width + self.value_text.x + 60

        super().tick(dt, state)

        self.value_text.y = self.alphabet.y - 7
        self.value_text.tick(dt)

    def draw(self, screen):
        super().draw(screen)
        
        self.value_text.draw(screen)