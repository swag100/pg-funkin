import pygame
from components.spritesheet import Spritesheet #not something that'd be directly imported to playstate, only components will import this
from components.conductor import Conductor
from .basestate import BaseState

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        #Default class variables; no need to override
        #self.persistent_data = {}
        #self.done = False
        #self.next_state = None

        #Make sprite group instead of just a list to contain game objects
        self.sheet = Spritesheet('assets/images/noteStrumline.png')

        self.conductor = Conductor(100, 0)


        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!
        voices = [
            pygame.mixer.Sound('assets/songs/bopeebo/Voices-dad.ogg'),
            pygame.mixer.Sound('assets/songs/bopeebo/Voices-bf.ogg')
        ]
        for i in range(len(voices)):
            pygame.mixer.Channel(i).play(voices[i])

        pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg') #Countdown handled out of this class? Maybe?
        pygame.mixer.music.play()
        #pygame.mixer.music.set_volume(0.5)
        
    def handle_event(self, event): 
        if event == pygame.event.Event(pygame.USEREVENT + 1): #BEAT HIT
            print("Beat hit",self.conductor.cur_beat)

            if self.conductor.cur_beat > -1: 
                if self.conductor.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()
    def tick(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: press = 'staticRight'
        elif keys[pygame.K_LEFT]: press = 'staticLeft'
        elif keys[pygame.K_UP]: press = 'staticUp'
        elif keys[pygame.K_DOWN]: press = 'staticDown'
        else: press = 'confirmHoldDown'

        self.note = self.sheet.load_animation(press)[0]
        self.note = pygame.transform.smoothscale_by(self.note, 0.7)

        self.conductor.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.note, self.note.get_rect())
