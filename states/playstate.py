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


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.sheet.animations['confirmRight'].play()
            if event.key == pygame.K_UP:
                self.sheet.animations['confirmUp'].play()
            if event.key == pygame.K_DOWN:
                self.sheet.animations['confirmDown'].play()
            if event.key == pygame.K_LEFT:
                self.sheet.animations['confirmLeft'].play()
        #if event.type == pygame.KEYUP:
        #    self.sheet.animations['staticDown'].play()

    def tick(self, dt):
        self.song.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.sheet.draw(screen, (0, 0))