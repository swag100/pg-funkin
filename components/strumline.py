import pygame
import settings
import math

from components.spritesheet import Spritesheet
from components.note import Note, Sustain

#GRAPHIC of individual receptor; handles VISUAL REPRESENTATION OF RECEPTOR
class StrumNote(pygame.sprite.Sprite):
    def __init__(self, strumline, id):
        pygame.sprite.Sprite.__init__(self)

        strum_spritesheet = Spritesheet('assets/images/noteStrumline.png', 0.7)

        #self.strumline = strumline
        self.strumline = strumline
        self.id = id #0,1,2,3,4,5,6,7
        self.direction = settings.DIRECTIONS[id % 4]

        #Hardcoded for now... Maybe add a json for this later? :)
        self.anim_offsets = {
            'static': (0, 0),
            'confirm': (-6, -6),
            'confirmHold': (-6, -6),
            'note': (18, 18),
            'press': (20, 20)
        }

        self.animations = strum_spritesheet.animations
        self.animation = None

        self.play_animation('static')
        self.update_position()

    def update_position(self):
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.id % 4 == 3: note_offset = (4, -2)

        #Implement anim offset:
        anim_offset = (0, 0)
        if self.anim_prefix in self.anim_offsets: anim_offset = self.anim_offsets[self.anim_prefix]

        self.pos = (
            self.strumline.pos[0] + anim_offset[0] + note_offset[0],
            self.strumline.pos[1] + anim_offset[1] + note_offset[1]
        )


    def play_animation(self, prefix, loop = False, start_time = None):
        if self.animation: self.animation.stop()

        self.anim_prefix = prefix
        self.animation = self.animations[prefix + self.direction.title()]

        self.animation.play(loop, start_time)

    def draw(self, screen):
        self.update_position()

        self.animation.blit(screen, self.pos)

#This is the STRUMLINE which manages every note passed to each strum GRAPHIC; this handles INPUT
class Strumline(object):
    def __init__(self, id, song):
        self.id = id #0,1,2,3,4,5,6,7
        self.conductor = song.conductor
        self.chart_reader = song.chart_reader

        self.name = settings.DIRECTIONS[self.id % 4]

        self.bot_strum = False
        if self.id > 3:
            self.bot_strum = True

        #Positioning
        strumline_offset = settings.PLAYER_STRUMLINE_OFFSET
        if self.bot_strum: strumline_offset = settings.OPPONENT_STRUMLINE_OFFSET

        self.pos = (
            strumline_offset[0] + (110 * (self.id % 4)),
            strumline_offset[1]
        )

        #Create strum note, load all notes for the strum from chart
        self.strum_note = StrumNote(self, id)

        self.notes = self.load_chart()[0]
        self.sustains = self.load_chart()[1]

    def load_chart(self): #Loads all notes for specific strum.
        notes = []
        sustains = []

        #generate regular notes
        speed = self.chart_reader.speed
        for note_data in self.chart_reader.chart[self.id]:
            time = int(note_data['t'])

            note = Note(self, time + settings.SONG_OFFSET, speed)
            notes.append(note)

            if 'l' in note_data:
                length = int(note_data['l'])
                if length > 0: #Is sustain note
                    height = math.floor(length / (self.conductor.crochet * 1000) * 4)

                    for i in range(height):
                        sustain_note = Sustain(self, time, i)
                        sustains.append(sustain_note)

                    sustain_note_end = Sustain(self, time, height, True)
                    sustains.append(sustain_note_end)

        return notes, sustains

    def handle_event(self, event):
        if self.bot_strum:
            if event.type == pygame.USEREVENT:
                if event.id == settings.BEAT_HIT:
                    if self.strum_note.animation.isFinished():
                        self.strum_note.play_animation('static')
            return

        if event.type == pygame.KEYDOWN:
            if event.key in settings.KEYBINDS[self.name]:
                #print(f'Attempted {self.name} note press')
                i_hit_a_note = False
                for note in self.notes:
                    #If notetime is in the range of 100 ms early or late of the position, you hit it.
                    for rating, hit_window in settings.HIT_WINDOWS.items():
                        hit_window_start_ms = self.conductor.song_position - (hit_window / 1000)
                        hit_window_end_ms = self.conductor.song_position + (hit_window / 1000)

                        if hit_window_start_ms <= note.time <= hit_window_end_ms:
                            self.notes.remove(note)
                            i_hit_a_note = True

                            pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = rating)) #Post rating event

                            break
                
                if i_hit_a_note: 
                    self.strum_note.play_animation('confirm')
                else:
                    self.strum_note.play_animation('press')

        if event.type == pygame.KEYUP:
            if event.key in settings.KEYBINDS[self.name]:
                #print(f'Attempted {self.name} note release')
                self.strum_note.play_animation('static')
                #for note in self.notes:
                #    if note.y <= 

    def tick(self, dt):
        for sustain in self.sustains:
            sustain.tick(dt)

            #Kill all sustains missed
            if sustain.y <= self.pos[1] - 200: self.sustains.remove(sustain)

            keys = pygame.key.get_pressed()
            if keys[settings.KEYBINDS[self.name][0]] or keys[settings.KEYBINDS[self.name][1]]:
                if sustain.time <= self.conductor.song_position: 
                    self.sustains.remove(sustain)
                    self.strum_note.play_animation('confirmHold')

            if self.bot_strum:
                if sustain.time <= self.conductor.song_position: 
                    self.sustains.remove(sustain)
                    self.strum_note.play_animation('confirmHold')

        for note in self.notes: 
            note.tick(dt)

            #Kill all notes that are missed
            if note.y <= self.pos[1] - 200: self.notes.remove(note)

            if self.bot_strum:
                if note.time <= self.conductor.song_position: 
                    self.notes.remove(note)
                    self.strum_note.play_animation('confirm')

    def draw(self, screen):
        self.strum_note.draw(screen)
        for sustain in self.sustains: sustain.draw(screen)
        for note in self.notes: note.draw(screen)