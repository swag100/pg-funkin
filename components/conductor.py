import pygame
import math
import settings

class Conductor(object): 
    def __init__(self, song, offset = 0): # Replace bpm, offset with song data in file and user offset preferences
        self.bpm = song.chart_reader.bpm
        self.crochet = 60 / self.bpm #Duration of beat in seconds

        self.offset = offset / 1000 #Add default offset: turn into milliseconds
        self.song_position = -self.crochet * 4

        self.cur_beat_time = None
        self.cur_beat = None #So it recognizes change on first beat

    def tick(self, dt):
        if self.offset > 0:
            self.offset -= dt
            return

        self.song_position += dt

        self.old_beat = self.cur_beat

        self.cur_beat_time = (self.song_position / self.crochet) - self.offset
        self.cur_beat = math.floor(self.cur_beat_time)

        if self.old_beat != self.cur_beat: #BEAT HIT
            self.old_beat = self.cur_beat
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{settings.BEAT_HIT}/{self.cur_beat}')) #Post BEAT HIT event