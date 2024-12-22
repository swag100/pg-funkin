import pygame
import os
import settings

from components.conductor import Conductor
from components.chart_reader import ChartReader

#Class containing any business to do with song audio playback.

class Song:
    def __init__(self, song_name, difficulty = 'normal'):
        self.song_name = song_name

        self.chart_reader = ChartReader(song_name, difficulty)

        self.characters = self.chart_reader.metadata['playData']['characters']
        self.bpm = self.chart_reader.bpm

        self.song_prefix = os.path.join('assets', 'songs', self.song_name)

        self.voices = [
            pygame.mixer.Sound(os.path.join(self.song_prefix, self.voices_name(self.characters['player']))),
            pygame.mixer.Sound(os.path.join(self.song_prefix, self.voices_name(self.characters['opponent'])))
        ]

        self.conductor = Conductor(self, settings.song_offset)

    def play_audio(self):
        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!

        for i in range(len(self.voices)):
            self.voices[i].set_volume(settings.volume)
            pygame.mixer.Channel(i).play(self.voices[i])
        
        inst_path = os.path.join(self.song_prefix, 'Inst.ogg')

        pygame.mixer.music.load(inst_path) 
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(settings.volume)
    
    def voices_name(self, singer):
        return f'Voices-{singer}.ogg' 