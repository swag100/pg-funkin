import pygame
import settings
import math

from components.spritesheet import Spritesheet

class Note(object):
    def __init__(self, strumline, time, speed):
        spritesheet = Spritesheet('assets/images/notes.png', 0.7)

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
    
        #animation
        self.animation = spritesheet.animations['note' + self.name.title()]
        self.animation.play()
    def tick(self, dt):
        self.y -= ((1000 * self.speed) / settings.SCROLL_SPEED_DIVISOR * dt)
    
    def draw(self, screen):
        if -self.animation.getMaxSize()[1] <= self.y <= settings.WINDOW_SIZE[1]: #in frame
            self.animation.blit(screen, (self.x, self.y))

class Sustain(object):
    def __init__(self, strumline, time, id, end = False):
        self.id = id

        self.strumline_id = strumline.id % 4
        self.speed = strumline.chart_reader.speed

        step_crochet = (strumline.conductor.crochet * 1000) / 4

        spritesheet = pygame.image.load('assets/images/NOTE_hold_assets.png')
        
        self.image = pygame.Surface.subsurface(spritesheet, pygame.Rect(104 * self.strumline_id, 0, 52, 1))
        self.image = pygame.transform.smoothscale(self.image, (52 * 0.7, step_crochet * 0.625))
        if end:
            self.image = pygame.Surface.subsurface(spritesheet, pygame.Rect(104 * self.strumline_id + 52, 0, 52, 64))
            self.image = pygame.transform.smoothscale_by(self.image, 0.7)

        time = time + (self.id * step_crochet)

        self.time = time / 1000

        self.x = strumline.pos[0] + 54
        self.y = (time * self.speed) / settings.SCROLL_SPEED_DIVISOR + 104

    def tick(self, dt):
        self.y -= ((1000 * self.speed) / settings.SCROLL_SPEED_DIVISOR * dt)
    
    def draw(self, screen):
        self.image.set_alpha(255 * 0.8)
        screen.blit(self.image, (self.x, self.y))