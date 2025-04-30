import pygame
import constants
from settings import settings

from components.spritesheet import Spritesheet

class Note(object):
    def __init__(self, strumline, time, speed):
        self.strumline = strumline
        self.time = (time / 1000) + strumline.conductor.song_position #Time in the song that the note should reach the strums; read from json.
        self.speed = 1 * speed #Scroll speed

        self.can_be_hit = True

        self.name = constants.DIRECTIONS[strumline.id % 4]

        self.x = self.strumline.pos[0]
        self.y = (time * speed) / constants.SCROLL_SPEED_DIVISOR

        #offsets
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.strumline.id % 4 == 3: note_offset = (4, -2)

        self.x += self.strumline.strum_note.anim_offsets['note'][0] + note_offset[0]
        self.y += self.strumline.strum_note.pos[1] + note_offset[1] + self.strumline.strum_note.anim_offsets['press'][1]

        self.y_change = (1000 * self.speed) / constants.SCROLL_SPEED_DIVISOR

        #downscroll
        self.downscroll_mult = ((not settings['preferences']['downscroll']) * 2) - 1

        self.y *= self.downscroll_mult
        self.y_change *= self.downscroll_mult
        if settings['preferences']['downscroll']:
            self.y += constants.DOWNSCROLL_STRUMLINE_Y_OFFSET * 2
            self.y += self.strumline.strum_note.animations['press' + self.strumline.strum_note.direction.title()].getMaxSize()[1]
    
        #animation
        spritesheet = Spritesheet('assets/images/strumline/notes.png', constants.STRUMLINE_SCALE_MULT)

        anim_frames = spritesheet.load_animation('note' + self.name.title())
        self.animation = spritesheet.frames_to_animation(anim_frames)
        
        self.animation.play()

    def tick(self, dt):
        self.y -= self.y_change * dt
    
    def draw(self, screen):
        if not self.can_be_hit:
            self.animation.grayscale()
            self.animation.set_alpha(128)
        
        self.animation.blit(screen, (self.x, self.y))

class Sustain(object):
    def __init__(self, note, length):
        self.true_id = note.strumline.id
        self.id = note.strumline.id % 4
        self.note = note #Note object this sustain will follow

        self.length = length

        self.being_eaten = False

        #Create graphic... Pretty ugly, I know
        
        spritesheet = pygame.image.load('assets/images/strumline/NOTE_hold_assets.png').convert_alpha()
        sheet_w = spritesheet.get_rect().w
        sheet_h = spritesheet.get_rect().h

        graphic_h = (self.length / constants.SCROLL_SPEED_DIVISOR) - (sheet_h / 2)
        if graphic_h < 0: 
            graphic_h = 0

        sus_sprite = pygame.Surface.subsurface(spritesheet, pygame.Rect(sheet_w / 4 * self.id, 0, sheet_w / 8, 1))
        sus_sprite = pygame.transform.smoothscale(sus_sprite, (sheet_w / 8 * constants.STRUMLINE_SCALE_MULT, graphic_h)) #64: height of note end sprite
        end_sprite = pygame.Surface.subsurface(spritesheet, pygame.Rect((sheet_w / 4) * self.id + (sheet_w / 8), 0, sheet_w / 8, sheet_h - 1))
        end_sprite = pygame.transform.smoothscale_by(end_sprite, constants.STRUMLINE_SCALE_MULT)

        sus_sprite_rect = sus_sprite.get_rect()
        end_sprite_rect = end_sprite.get_rect()

        self.image = pygame.Surface((sus_sprite_rect.w, sus_sprite_rect.h + end_sprite_rect.h), pygame.SRCALPHA)
        self.image.blit(sus_sprite, (0, 0))
        self.image.blit(end_sprite, (0, sus_sprite_rect.h))

        #Define position
        note_graphic_size = self.note.animation.getMaxSize()

        self.x = note.x + (note_graphic_size[0] / 2) - (self.image.get_rect().w / 2)
        self.y = note.y + (note_graphic_size[1] / 2)

        if settings['preferences']['downscroll']:
            self.image = pygame.transform.flip(self.image, False, True)
            self.y -= (self.image.get_rect().h)

        self.y_change = self.note.y_change
    
    def eat(self, dt): #Stupid name; this handles holding sustains down
        self.being_eaten = True

        self.y += self.y_change * dt
        self.length -= (self.y_change * dt * 2) * self.note.downscroll_mult

        image_rect = self.image.get_rect()
        new_image = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        new_image.blit(self.image, (0, -self.y_change * dt))

        self.image = new_image

    def tick(self, dt):
        self.y -= self.y_change * dt
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))