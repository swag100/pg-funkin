import pygame
from .basestate import BaseState

from components.spritesheet import Spritesheet #not something that'd be directly imported to playstate, only components will import this
from components.song import Song
from components.conductor import Conductor

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        self.song = Song('bopeebo')

        #Default class variables; no need to override
        #self.persistent_data = {}
        #self.done = False
        #self.next_state = None

        #Make sprite group instead of just a list to contain game objects
        self.sheet = Spritesheet('assets/images/noteStrumline.png', 0.7)

        #LOADING MUSIC... MAYBE MOVE SOMEWHERE ELSE
        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!

        self.song.start()
        
    def handle_event(self, event): 
        if event == pygame.event.Event(pygame.USEREVENT + 1): #BEAT HIT
            # print("Beat hit",self.conductor.cur_beat)

            if self.song.conductor.cur_beat > -1: 
                if self.song.conductor.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()
    def tick(self, dt):
        self.song.tick(dt)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: press = 'confirmHoldRight'
        elif keys[pygame.K_LEFT]: press = 'confirmHoldLeft'
        elif keys[pygame.K_UP]: press = 'confirmHoldUp'
        elif keys[pygame.K_DOWN]: press = 'confirmHoldDown'
        else: press = 'staticDown'

        self.note = self.sheet.animations[press][int(dt * 11000) % len(self.sheet.animations[press])]
        self.note_data = self.sheet.frame_data[press][int(dt * 11000) % len(self.sheet.animations[press])]

    def draw(self, screen):
        screen.fill((255, 255, 255))

        note_rect = self.note.get_rect().move(self.note_data['frameX'],self.note_data['frameY'])
        screen.blit(self.note, note_rect)