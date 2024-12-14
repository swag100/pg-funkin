import pygame
import xmltodict
import math

class Conductor(object): 
    def __init__(self, bpm, offset):
        self.bpm = bpm
        self.crochet = 60 / bpm #Duration of beat in seconds

        self.song_position = -offset / 1000 #milliseconds
        self.cur_beat_time = 0
        self.cur_beat = 0

    def tick(self, dt):
        self.song_position += dt

        self.old_beat = self.cur_beat

        self.cur_beat_time = (self.song_position / self.crochet)
        self.cur_beat = math.floor(self.cur_beat_time)

        if self.old_beat != self.cur_beat: #BEAT HIT
            self.old_beat = self.cur_beat

            if self.song_position >= 0: 
                #Apply song offset to BEAT HITS only, not playing the song;
                #Song will be handled outside of this class? Maybe not. still deciding
                if self.cur_beat == 0:
                    pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg')
                    pygame.mixer.music.play()

                if self.cur_beat % 4 == 0:
                    pygame.mixer.Sound("assets/sounds/metronome1.ogg").play()
                else:
                    pygame.mixer.Sound("assets/sounds/metronome2.ogg").play()