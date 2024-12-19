import pygame
import settings

from components.spritesheet import Spritesheet

class Note(object):
    def __init__(self, strumline, time, speed):
        self.strumline = strumline
        self.time = time / 1000 #Time in the song that the note should reach the strums; read from json.
        self.speed = 1 * speed #Scroll speed

        self.name = settings.DIRECTIONS[strumline.id % 4]

        self.x = self.strumline.pos[0]
        self.y = (time) * speed / settings.SCROLL_SPEED_DIVISOR

        #offsets
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.strumline.id % 4 == 3: note_offset = (4, -2)

        self.x += self.strumline.strum_note.anim_offsets['note'][0] + note_offset[0]
        self.y += self.strumline.strum_note.pos[1] + note_offset[1] + self.strumline.strum_note.anim_offsets['press'][1]

        self.y_change = (1000 * self.speed) / settings.SCROLL_SPEED_DIVISOR
    
        #animation
        spritesheet = Spritesheet('assets/images/notes.png', settings.STRUMLINE_SCALE_MULT)

        anim_frames = spritesheet.load_animation('note' + self.name.title())
        self.animation = spritesheet.frames_to_animation(anim_frames)
        
        self.animation.play()

    def tick(self, dt):
        self.y -= self.y_change * dt
    
    def draw(self, screen):
        if -self.animation.getMaxSize()[1] <= self.y <= settings.WINDOW_SIZE[1]: #in frame
            self.animation.blit(screen, (self.x, self.y))

class Sustain(object):
    def __init__(self, note, length):
        self.id = note.strumline.id % 4
        self.note = note #Note object this sustain will follow

        self.length = length

        #Create graphic... Pretty ugly, I know
        
        spritesheet = pygame.image.load('assets/images/NOTE_hold_assets.png').convert_alpha()
        sheet_w = spritesheet.get_rect().w

        sus_sprite = pygame.Surface.subsurface(spritesheet, pygame.Rect(sheet_w / 4 * self.id, 0, sheet_w / 8, 1))
        sus_sprite = pygame.transform.smoothscale(sus_sprite, (sheet_w / 8 * settings.STRUMLINE_SCALE_MULT, self.length / 2)) #64: height of note end sprite
        end_sprite = pygame.Surface.subsurface(spritesheet, pygame.Rect((sheet_w / 4) * self.id + (sheet_w / 8), 0, sheet_w / 8, 64))
        end_sprite = pygame.transform.smoothscale_by(end_sprite, settings.STRUMLINE_SCALE_MULT)

        sus_sprite_rect = sus_sprite.get_rect()
        end_sprite_rect = end_sprite.get_rect()

        self.image = pygame.Surface((sus_sprite_rect.w, sus_sprite_rect.h + end_sprite_rect.h), pygame.SRCALPHA)
        self.image.blit(sus_sprite, (0, 0))
        self.image.blit(end_sprite, (0, sus_sprite_rect.h))

        #Define position
        note_graphic_size = self.note.animation.getMaxSize()

        self.x = note.x + (note_graphic_size[0] / 2) - (self.image.get_rect().w / 2)
        self.y = note.y + (note_graphic_size[1] / 2)

        self.y_change = self.note.y_change
    
    def eat(self, dt): #Stupid name; this handles holding sustains down
        self.y += self.y_change * dt

        image_rect = self.image.get_rect()
        new_image = pygame.Surface((image_rect.w, image_rect.h), pygame.SRCALPHA)
        new_image.blit(self.image, (0, -self.y_change * dt))

        self.image = new_image

    def tick(self, dt):
        self.y -= self.y_change * dt
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))