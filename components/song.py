import pygame
import os
import settings

from components.conductor import Conductor
from components.chart_reader import ChartReader

#Class containing any business to do with the song. Also health, score, accuracy

class Song:
    def __init__(self, song_name, difficulty = 'normal'):
        self.song_name = song_name

        self.chart_reader = ChartReader(song_name, difficulty)

        self.characters = self.chart_reader.metadata['playData']['characters']
        self.bpm = self.chart_reader.bpm

        self.conductor = Conductor(self, settings.SONG_OFFSET)

    def start(self):

        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!
        voices = [
            pygame.mixer.Sound(self.song_path(self.characters['player'])),
            pygame.mixer.Sound(self.song_path(self.characters['opponent']))
        ]
        for i in range(len(voices)):
            pygame.mixer.Channel(i).play(voices[i])
            voices[i].set_volume(settings.volume)

        pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg') 
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(settings.volume)
    
    def song_path(self, singer):
        return os.path.join('assets', 'songs', self.song_name, f'Voices-{singer}.ogg')