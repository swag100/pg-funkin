import pygame
import math
import settings

class Conductor(object): 
    def __init__(self, song, offset = 0): # Replace bpm, offset with song data in file and user offset preferences
        self.bpm = song.chart_reader.bpm
        self.crochet = 60 / self.bpm #Duration of beat in seconds

        self.offset = (offset + 1) / 1000 #Add default offset: turn into milliseconds
        self.song_position = -self.offset 

        self.cur_beat_time = 0

        #countdown
        self.cur_beat = -1 #So it recognizes change on first beat

    def tick(self, dt):
        if self.offset > 0:
            self.offset -= dt
            return

        self.song_position += dt

        self.old_beat = self.cur_beat

        self.cur_beat_time = self.song_position / self.crochet
        self.cur_beat = math.floor(self.cur_beat_time)

        if self.old_beat != self.cur_beat: #BEAT HIT
            self.old_beat = self.cur_beat
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = settings.BEAT_HIT)) #Post BEAT HIT event