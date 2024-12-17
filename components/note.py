import pygame
import settings

from components.spritesheet import Spritesheet

class Sustain(pygame.sprite.Sprite): #Work on this later
    pass

class Note(object):
    speed_divisor = 2.1

    def __init__(self, strumline, time, speed, length):
        spritesheet = Spritesheet('assets/images/notes.png', 0.7)

        self.strumline = strumline
        self.time = time #Time in the song that the note should reach the strums; read from json.
        self.speed = 1 * speed #Scroll speed
        self.length = length #If 0, no sustain; otherwise generate sustain this many milliseconds

        self.name = settings.DIRECTIONS[strumline.id % 4]

        self.x = self.strumline.pos[0]
        self.y = time * speed / self.speed_divisor

        #offsets
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.strumline.id % 4 == 3: note_offset = (4, -2)

        self.x += self.strumline.strum_note.anim_offsets['press'][0] + note_offset[0]
        self.y += self.strumline.strum_note.pos[1] + note_offset[1] + self.strumline.strum_note.anim_offsets['press'][1]
    
        self.animation = spritesheet.animations['note' + self.name.title()]
        self.animation.play()
    def tick(self, dt):
        self.y -= ((1000 * self.speed) / self.speed_divisor * dt)
    
    def draw(self, screen):
        if -self.animation.getMaxSize()[1] <= self.y <= settings.WINDOW_SIZE[1]: #in frame
            self.animation.blit(screen, (self.x, self.y))

    def __str__(self):
        return f'{self.name.title()} at ({self.x}, {self.y})'