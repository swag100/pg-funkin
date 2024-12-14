import pygame
import math

class Conductor(object): 
    def __init__(self, bpm, offset = 0): # Replace bpm, offset with song data in file and user offset preferences
        self.bpm = bpm
        self.crochet = 60 / bpm #Duration of beat in seconds

        self.offset = (offset + 3) / 1000 #Add default offset: turn into milliseconds
        self.song_position = -self.offset 

        self.cur_beat_time = 0
        self.cur_beat = -1 #So it recognizes change on first beat

        pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg') #Countdown handled out of this class? Maybe?
        pygame.mixer.music.play()

    def tick(self, dt):
        self.song_position += dt

        self.old_beat = self.cur_beat

        self.cur_beat_time = self.song_position / self.crochet
        self.cur_beat = math.floor(self.cur_beat_time)

        if self.old_beat != self.cur_beat: #BEAT HIT
            self.old_beat = self.cur_beat
            
            if self.cur_beat > -1: 
                if self.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()

            print(self.cur_beat)