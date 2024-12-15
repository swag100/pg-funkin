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

        self.conductor = Conductor(100, 0)

        #Make sprite group instead of just a list to contain game objects
        self.sheet = Spritesheet('assets/images/noteStrumline.png', 0.7)

        #LOADING MUSIC... MAYBE MOVE SOMEWHERE ELSE
        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!
        voices = [
            pygame.mixer.Sound('assets/songs/bopeebo/Voices-dad.ogg'),
            pygame.mixer.Sound('assets/songs/bopeebo/Voices-bf.ogg')
        ]
        for i in range(len(voices)):
            pygame.mixer.Channel(i).play(voices[i])
            voices[i].set_volume(1)

        pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg') #Countdown handled out of this class? Maybe?
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)
        
    def handle_event(self, event): 
        if event == pygame.event.Event(pygame.USEREVENT + 1): #BEAT HIT
            # print("Beat hit",self.conductor.cur_beat)

            if self.conductor.cur_beat > -1: 
                if self.conductor.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()
    def tick(self, dt):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: press = 'confirmHoldRight'
        elif keys[pygame.K_LEFT]: press = 'confirmHoldLeft'
        elif keys[pygame.K_UP]: press = 'confirmHoldUp'
        elif keys[pygame.K_DOWN]: press = 'confirmHoldDown'
        else: press = 'staticDown'

        self.note = self.sheet.animations[press][int(dt * 10000) % len(self.sheet.animations[press])]
        self.note_data = self.sheet.frame_data[press][int(dt * 10000) % len(self.sheet.animations[press])]
        

        self.conductor.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        note_rect = self.note.get_rect().move(-self.note_data['frameX'],-self.note_data['frameY'])
        screen.blit(self.note, note_rect)
