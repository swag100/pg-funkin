import pygame
import settings

from components.spritesheet import Spritesheet
from components.note import Note, Sustain

#GRAPHIC of individual receptor; handles VISUAL REPRESENTATION OF RECEPTOR
class StrumNote(pygame.sprite.Sprite):
    def __init__(self, strumline, id):
        pygame.sprite.Sprite.__init__(self)

        spritesheet = Spritesheet('assets/images/noteStrumline.png', 0.7)

        #self.strumline = strumline
        self.strumline = strumline
        self.id = id #0,1,2,3,4,5,6,7
        self.direction = settings.DIRECTIONS[id % 4]

        #Hardcoded for now... Maybe add a json for this later? :)
        self.anim_offsets = {
            'static': (0, 0),
            'confirm': (-6, -6),
            'confirmHold': (-6, -6),
            'press': (18, 18)
        }

        self.animations = spritesheet.animations
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

    def handle_event(self, event):
        #replace these with userevents; i.e. NOTE_HIT, NOTE_MISS, NOTE_MISS_RELEASE?
        if event.type == pygame.KEYDOWN:
            if event.key in settings.KEYBINDS[self.direction]:
                self.play_animation('press')
        if event.type == pygame.KEYUP:
            if event.key in settings.KEYBINDS[self.direction]:
                self.play_animation('static')

    def draw(self, screen):
        self.update_position()

        self.animation.blit(screen, self.pos)

#This is the STRUMLINE which manages every note passed to each strum GRAPHIC.
class Strumline(object):
    def __init__(self, id, chart_reader):
        self.id = id #0,1,2,3,4,5,6,7
        self.chart_reader = chart_reader

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
        self.notes = self.load_notes()

    def load_notes(self): #Loads all notes for specific strum.
        notes = []
        for note_data in self.chart_reader.chart[self.id]:
            time = int(note_data['t'])
            speed = self.chart_reader.speed

            length = 0
            if 'l' in note_data: length = int(note_data['l'])

            note = Note(self, time + settings.SONG_OFFSET, speed, length)
            notes.append(note)

        return notes

    def handle_event(self, event):
        if self.bot_strum:
            if event.type == pygame.USEREVENT:
                if event.id == settings.BEAT_HIT:
                    if self.strum_note.animation.isFinished():
                        self.strum_note.play_animation('static')
            return

        #animation
        self.strum_note.handle_event(event)

    def tick(self, dt):
        for note in self.notes: 
            note.tick(dt)

            #Kill all notes that are missed
            if note.y <= self.pos[1] - 200: self.notes.remove(note)

            if self.bot_strum:
                if note.y <= self.pos[1] + 24: 
                    self.notes.remove(note)
                    self.strum_note.play_animation('confirm')

    def draw(self, screen):
        self.strum_note.draw(screen)
        for note in self.notes: note.draw(screen)