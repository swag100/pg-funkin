import pygame
import json
import os

from components.conductor import Conductor

#Class that handles song playback; this includes conductor, audio files

class Song:
    def __init__(self, name, difficulty = 'normal'):
        self.song_name = name

        metadata_path = os.path.join('assets', 'data', name, f'{name}-metadata.json')
        with open(metadata_path) as metadata_file:
            self.metadata = json.loads(metadata_file.read())
        metadata_file.close()

        play_data = self.metadata['playData']

        self.characters = play_data['characters']
        self.difficulty = play_data['difficulties'][0] #Default to first item
        if self.difficulty in play_data['difficulties']: self.difficulty = difficulty

        self.time_changes = self.metadata['timeChanges']
        self.start_bpm = self.time_changes[0]['bpm']
        self.bpm = self.start_bpm

    def start(self):
        self.conductor = Conductor(self.bpm) #Before conductor, do countdown? Handle countdown in conductor?

        voices = [
            pygame.mixer.Sound(self.song_path(self.characters['player'])),
            pygame.mixer.Sound(self.song_path(self.characters['opponent']))
        ]
        for i in range(len(voices)):
            pygame.mixer.Channel(i).play(voices[i])
            #voices[i].set_volume(1)

        pygame.mixer.music.load('assets/songs/bopeebo/Inst.ogg') 
        pygame.mixer.music.play()
        #pygame.mixer.music.set_volume(1)
    
    def song_path(self, singer):
        return os.path.join('assets', 'songs', self.song_name, f'Voices-{singer}.ogg')
    
    def tick(self, dt):
        self.conductor.tick(dt)