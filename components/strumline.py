import pygame
import constants
from settings import settings

from threading import Thread
from components.spritesheet import Spritesheet
from components.note import Note, Sustain
from components.strum_effects import NoteSplash, HoldCover, ReleaseSplash

#Constants for state detecton.
PRESSED = 'pressed' #Will enter after a successful hit, no matter the rating
HOLDING = 'holding' #Can only enter after being in pressed state for a frame
RELEASED = 'released' #Entered for a frame during release

#GRAPHIC of individual receptor; handles VISUAL REPRESENTATION OF RECEPTOR
class StrumNote(pygame.sprite.Sprite):
    def __init__(self, strumline, id):
        pygame.sprite.Sprite.__init__(self)

        strum_spritesheet = Spritesheet('assets/images/strumline/noteStrumline.png', constants.STRUMLINE_SCALE_MULT)
        strum_spritesheet.preload_animations()

        #self.strumline = strumline
        self.strumline = strumline
        self.id = id #0,1,2,3,4,5,6,7
        self.direction = constants.DIRECTIONS[id % 4]

        #Hardcoded for now... Maybe add a json for this later? :)
        #Also, these are not scaleable. make them relative later? Multiply these by 1.3?
        self.anim_offsets = {
            'static': (0, 0),
            'confirm': (-6, -6),
            'confirmHold': (-6, -6),
            'note': (18, 18),
            'press': (20, 20)
        }

        self.anim_time = 0 #How much time has this animation been playing
        self.animations = strum_spritesheet.animations
        self.animations['confirmHold' + self.direction.title()].reverse()
        self.animation = None

        self.play_animation('static')
        self.pos = self.position('static')

    def position(self, prefix):
        #Hardcode right note offset.
        note_offset = (0, 0)
        if self.id % 4 == 3: note_offset = (4, -2)

        #Implement anim offset:
        anim_offset = (0, 0)
        if prefix in self.anim_offsets: anim_offset = self.anim_offsets[prefix]

        return (
            self.strumline.pos[0] + anim_offset[0] + note_offset[0],
            self.strumline.pos[1] + anim_offset[1] + note_offset[1]
        )


    def play_animation(self, prefix, loop = False, start_time = None):
        if self.animation: self.animation.stop()

        self.anim_time = 0 #How much time has this animation been playing

        self.anim_prefix = prefix
        self.animation = self.animations[prefix + self.direction.title()]

        self.animation.play(loop, start_time)

    def draw(self, screen):
        self.pos = self.position(self.anim_prefix)

        self.animation.blit(screen, self.pos)

#This is the STRUMLINE which manages every note passed to each strum GRAPHIC; this handles INPUT
class Strumline(object):
    def __init__(self, id, song):
        self.id = id #0,1,2,3,4,5,6,7
        self.conductor = song.conductor
        self.chart_reader = song.chart_reader

        self.name = constants.DIRECTIONS[self.id % 4]

        self.state = None #Strumline state, either PRESSED, HOLDING, or RELEASED, or None.

        self.bot_strum = False
        if self.id > 3 and not settings['preferences']['two player'] or settings['preferences']['botplay']:
            self.bot_strum = True

        #Positioning
        strumline_offset = constants.PLAYER_STRUMLINE_OFFSET
        if self.id > 3: strumline_offset = constants.OPPONENT_STRUMLINE_OFFSET

        self.pos = [
            strumline_offset[0] + (110 * (self.id % 4)),
            strumline_offset[1]
        ]

        #downscroll
        if settings['preferences']['downscroll']:
            self.pos[1] += constants.DOWNSCROLL_STRUMLINE_Y_OFFSET

        #Create strum note, load all notes for the strum from chart
        self.strum_note = StrumNote(self, id)

        self.notes = self.load_chart()[0]
        self.sustains = self.load_chart()[1]

        #lists containing fx for drawing; seperated for convenience
        self.hold_cover = None
        self.splashes = []

    def load_chart(self): #Loads all notes for specific strum.
        notes = []
        sustains = []

        #generate regular notes
        speed = self.chart_reader.speed
        for note_data in self.chart_reader.chart[self.id]:
            note = Note(self, int(note_data['t']) - (self.conductor.song_position * 1000), speed)
            notes.append(note)

            if 'l' in note_data:
                sustain = Sustain(note, int(note_data['l']))
                sustains.append(sustain)

        return notes, sustains

    def note_in_hit_window(self, note, hit_window):
        hit_window_start_ms = self.conductor.song_position - (hit_window / 1000)
        hit_window_end_ms = self.conductor.song_position + (hit_window / 1000)

        value = hit_window_start_ms <= note.time <= hit_window_end_ms
        
        return value

    def get_rating(self, note):
        for rating, hit_window in constants.HIT_WINDOWS.items():
            if self.note_in_hit_window(note, hit_window):
                return rating

    def make_splash(self, rating):
        if rating in ['perfect', 'killer', 'sick']:
            def do_splash(strumline):
                strumline.splashes.append(NoteSplash(self))

            Thread(target = do_splash, args = (self,)).start()

    def handle_event(self, event):
        if self.state == PRESSED:
            self.state = HOLDING
        if self.state != HOLDING:
            self.state = None

        if self.bot_strum: return
                
        if event.type == pygame.KEYDOWN:
            condition = event.key in settings['keybinds'][self.name]
            if settings['preferences']['two player']: 
                if self.id <= 3: 
                    condition = event.key == settings['keybinds'][self.name][1]
                else:
                    condition = event.key == settings['keybinds'][self.name][0]

            if condition:
                self.strum_note.play_animation('press')

                for note in self.notes:
                    hit_window = list(constants.HIT_WINDOWS.items())[-1][1]
                    if self.note_in_hit_window(note, hit_window) and note.can_be_hit:
                        self.state = PRESSED
                        
                        rating = self.get_rating(note)
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_GOOD_HIT}/{rating}/{self.id}')) #Post rating event
                        
                        self.make_splash(rating)

                        
                        #bad note
                        if rating in ['shit', 'bad']:
                            #note.animation.getCurrentFrame().fill((255, 255, 255, 128), special_flags = pygame.BLEND_RGBA_MULT) 
                            #note.animation.getCurrentFrame().fill((128, 128, 128), special_flags = pygame.BLEND_RGB_ADD) 
                            note.can_be_hit = False
                        else:
                            self.notes.remove(note)
                        #TODO: work on bad notes. 
                        # If player hits incorrect note at the right time, that note will turn into bad note, and note miss event will fire.
                        # Make them look pretty.
                        
                        
                        #self.notes.remove(note)

                        self.strum_note.play_animation('confirm') #Override animation
                
                #If there was no press detected, it's a GHOST miss!
                if self.state != PRESSED:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_MISS}/ghost miss/{self.id}')) #feels too slow
                    #pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = 'miss'))

        if event.type == pygame.KEYUP:
            if event.key in settings['keybinds'][self.name]:
                if self.state != None:
                    self.state = RELEASED

                self.strum_note.play_animation('static')

    def tick(self, dt):
        for sustain in self.sustains: 
            sustain.tick(dt)

            if sustain.note.time <= self.conductor.song_position and sustain.note.can_be_hit: 
                if self.bot_strum or self.state == HOLDING:
                    sustain.eat(dt)

                    if not self.hold_cover:
                        self.hold_cover = HoldCover(sustain)

                    if self.strum_note.animation.isFinished() and self.strum_note.anim_prefix != 'confirmHold':
                        self.strum_note.play_animation('confirmHold')

                    if sustain.length <= 0:
                        self.sustains.remove(sustain)
                        
                        self.state = RELEASED

                        self.hold_cover = None
                        if not self.bot_strum:
                            self.splashes.append(ReleaseSplash(self))

                        self.strum_note.play_animation('press')
                        if self.bot_strum: 
                            self.strum_note.play_animation('static')

                    self.strum_note.anim_time = 0 #for bot strum animation
                else:
                    if self.state == RELEASED:
                        self.sustains.remove(sustain)
                        self.hold_cover = None

                        if sustain.length <= ((self.conductor.crochet * 1000) / 4) + 2:
                            self.splashes.append(ReleaseSplash(self))

                        """
                        else: 
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_MISS}/hold miss/{self.id % 4}')) #Post rating event
                            #This is a HOLD miss; it was let go prematurely. Will play sound but won't remove health!
                        """

            #if sustain was not eaten after 2 seconds: Delete it!
            if sustain.note.time + ((sustain.length * 2) / 1000) + 2 <= self.conductor.song_position: 
                try:
                    self.sustains.remove(sustain)
                except:
                    print(sustain, 'dropped')

        for note in self.notes: 
            note.tick(dt)

            if self.bot_strum:
                if note.time <= self.conductor.song_position:
                    if self.id <= 3:
                        rating='perfect'
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_GOOD_HIT}/{rating}/{self.id}')) #Post rating event
                        self.make_splash(rating)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_BOT_PRESS}//{self.id}')) #Post rating event 
                    self.state = PRESSED
                    self.notes.remove(note)
                    self.strum_note.play_animation('confirm')

            #Miss all notes that are late by 2 steps or over
            if note.time + (self.conductor.crochet / 2) <= self.conductor.song_position and note.can_be_hit: 
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, id = f'{constants.NOTE_MISS}/miss/{self.id}')) #Post rating event
                self.notes.remove(note)
        
        self.strum_note.anim_time += dt

        strumnote_reset_time = self.conductor.crochet / 2
        if self.conductor.bpm > 120:
            strumnote_reset_time = self.conductor.crochet

        if self.strum_note.anim_time >= strumnote_reset_time:
            if self.bot_strum:
                self.state = RELEASED
                self.strum_note.play_animation('static')
            else:
                if 'confirm' in self.strum_note.anim_prefix:
                    self.strum_note.play_animation('press')
            


        #for hold note effects(Stupid)
        if self.hold_cover: self.hold_cover.tick(dt)

        for splash in self.splashes:
            splash.animation.tickFrameNum()
            if splash.animation.isFinished():
                self.splashes.remove(splash)

        #so that the strum note's animations update
        self.strum_note.animation.tickFrameNum()
        if self.hold_cover: self.hold_cover.animation.tickFrameNum()
                
    def draw(self, screen):
        self.strum_note.draw(screen)
        
        for sustain in self.sustains: sustain.draw(screen)
        if self.hold_cover: self.hold_cover.draw(screen)
        for note in self.notes: note.draw(screen)
        for splash in self.splashes: splash.draw(screen)