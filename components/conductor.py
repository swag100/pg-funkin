import pygame
import xmltodict

class Conductor(object): 
    def __init__(self, bpm, offset):
        self.bpm = bpm
        self.crochet = 60 / bpm #Duration of beat in seconds

        self.song_position = -offset / 1000
        self.cur_beat_time = 0

        self.cur_beat = 0
    def tick(self, dt):
        self.song_position += dt
        if self.song_position > self.cur_beat_time + (self.crochet):
            self.cur_beat_time += self.crochet

        self.cur_beat = self.cur_beat_time / self.crochet
        if self.cur_beat % 4 == 0:
            pass #play high beep
        else:
            pass #play low beep

        print(int(round(self.cur_beat, 2)))