import pygame
import constants

from components.conductor import Conductor
from components.chart_reader import ChartReader

#Class containing any business to do with song audio playback.

class Song:
    def __init__(self, song_name, difficulty = 'normal'):
        self.song_name = song_name

        self.chart_reader = ChartReader(song_name, difficulty)

        self.stage = self.chart_reader.metadata['playData']['stage']
        self.characters = self.chart_reader.metadata['playData']['characters']
        self.bpm = self.chart_reader.bpm

        self.song_prefix = f'assets/songs/{self.song_name}/'
        self.voices = [
            pygame.mixer.Sound(self.song_prefix+self.voices_name(self.characters['player'])),
            pygame.mixer.Sound(self.song_prefix+self.voices_name(self.characters['opponent']))
        ]

        self.inst_path = f'{self.song_prefix}/Inst.ogg'
        self.song_length = pygame.mixer.Sound(self.inst_path).get_length()

        self.conductor = Conductor(self, constants.SETTINGS_DEFAULT_SONG_OFFSET)

        self.paused = False

    def play_audio(self):
        #FIGURED IT OUT... THIS IS THE CORRECT ORDER!
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = constants.SONG_BEGAN)) #Post rating event

        for i in range(len(self.voices)):
            pygame.mixer.Channel(i).play(self.voices[i])

        pygame.mixer.music.load(self.inst_path) 
        pygame.mixer.music.play()

    def stop_audio(self):
        for i in range(len(self.voices)):
            pygame.mixer.Channel(i).stop()

        pygame.mixer.music.stop()

    def toggle_pause(self): 
        if self.paused:
            pygame.mixer.music.unpause()
            for i in range(len(self.voices)):
                pygame.mixer.Channel(i).unpause()
        else:
            pygame.mixer.music.pause()
            for i in range(len(self.voices)):
                pygame.mixer.Channel(i).pause()

        self.paused = not self.paused

    def is_finished(self):
        return self.conductor.song_position >= self.song_length
    
    def voices_name(self, singer):
        return f'Voices-{singer}.ogg' 
    
    def tick(self, dt, player_voice_track_muted = False):
        self.conductor.tick(dt)

        pygame.mixer.music.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
        for i in range(len(self.voices)):
            self.voices[i].set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
        if player_voice_track_muted:
            self.voices[0].set_volume(0)

        #TODO: Check to see if each audio file's audio position is synced with the song. Then, if it isn't, re-sync it!

        if self.is_finished():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.SONG_ENDED}/{dt}')) #Post rating event