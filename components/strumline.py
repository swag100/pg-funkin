import pygame
import settings

from components.spritesheet import Spritesheet

#graphic of individual receptor; handles animations
class StrumlineNote(pygame.sprite.Sprite):
    def __init__(self, strumline, direction):
        pygame.sprite.Sprite.__init__(self)

        self.strumline = strumline
        self.direction = direction
        self.direction_id = settings.DIRECTIONS.index(direction)

        self.anim_offsets = {
            'static': (0, 0),
            'confirm': (-6, -6),
            'confirmHold': (-6, -6),
            'press': (20, 20)
        }

        self.animations = Spritesheet('assets/images/noteStrumline.png', 0.7).animations
        self.animation = None

        self.play_animation('static')

    def play_animation(self, prefix, loop = False, start_time = None):
        if self.animation: self.animation.stop()

        self.anim_prefix = prefix
        self.animation = self.animations[prefix + self.direction.title()]

        self.animation.play(loop, start_time)

    def handle_event(self, event):
        if self.strumline.bot_play: return

        if event.type == pygame.KEYDOWN:
            if event.key in settings.KEYBINDS[self.direction]:
                self.play_animation('press')
        if event.type == pygame.KEYUP:
            if event.key in settings.KEYBINDS[self.direction]:
                self.play_animation('static')

    def draw(self, screen):
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.direction_id == 3: note_offset = (4, -2)

        #Implement anim offset:
        anim_offset = (0, 0)
        if self.anim_prefix in self.anim_offsets: anim_offset = self.anim_offsets[self.anim_prefix]

        pos = (
            self.strumline.pos[0] + anim_offset[0] + note_offset[0] + (110 * self.direction_id),
            self.strumline.pos[1] + anim_offset[1] + note_offset[1]
        )

        self.animation.blit(screen, pos)

#Group of 4 individual StrumlineNote objects
class Strumline(pygame.sprite.Sprite):
    def __init__(self, pos, bot_play):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.bot_play = bot_play#Will this strumline take in player input?
        
        self.strums = []
        for direction in settings.DIRECTIONS:
            self.strums.append(StrumlineNote(self, direction))
    
    def handle_event(self, event):
        for strum in self.strums: strum.handle_event(event)
            
    def draw(self, screen): #Draw strums
        for strum in self.strums: strum.draw(screen)