import pygame
import constants
import settings
import json

from components.spritesheet import Spritesheet

class Character:
    def __init__(self, play_state, character, pos, character_type = 'girlfriend'):
        self.play_state = play_state
        self.character = character #string of character name.
        self.screen_pos = pos #Location this character will be drawn at, offsets will be applied to this.

        self.character_type = character_type

        self.metadata = self.load_metadata() #character data read from its json File.
        self.name = self.metadata['name']

        self.sing_time = 8 #Afaik, we don't use this.
        if 'singTime' in self.metadata:
            self.sing_time = self.metadata['singTime']

        self.flip_x = False
        if 'flipX' in self.metadata:
            self.flip_x = self.metadata['flipX']

        #Sort character's metadata into dictionaries.
        #This includes an offset dictionary, and an animation dictionary
        metadata_animations = self.metadata['animations']

        #print(character)
        spritesheet = Spritesheet('assets/images/'+self.metadata['assetPath']+'.png')

        self.offsets_dict = {}
        self.animations_dict = {}
        for item in metadata_animations:
            name = item['name']

            self.offsets_dict[name] = item['offsets']

            if 'assetPath' in item:
                spritesheet = Spritesheet('assets/images/'+item['assetPath']+'.png')

            anim_frames = spritesheet.load_anim_frames(item['prefix'])

            animation = spritesheet.frames_to_animation(anim_frames)
            animation.flip(self.flip_x, False)
            
            self.animations_dict[name] = animation

        self.anim_prefix = 'idle'
        if 'startingAnimation' in self.metadata:
            self.anim_prefix = self.metadata['startingAnimation']

        self.animation = self.animations_dict[self.anim_prefix]

        self.max_idle_size = self.animation.getMaxSize()
        self.screen_pos[0] -= self.max_idle_size[0] / 2
        self.screen_pos[1] -= self.max_idle_size[1]

        self.animation.play()

    def play_animation(self, prefix, loop = False, start_time = None):
        if prefix not in self.animations_dict: return #failsafe

        self.animation.stop()

        self.anim_prefix = prefix
        self.animation = self.animations_dict[prefix]

        self.animation.play(loop, start_time)

    def load_metadata(self):
        metadata_path = f'assets/data/characters/{self.character}.json'
        with open(metadata_path) as metadata_file:
            metadata = json.loads(metadata_file.read())
        metadata_file.close()

        return metadata
    
    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            event_list = event.id.split('/', 1)
            event_type = event_list[0]
            try:
                event_parameters = event_list[1].split('/')
            except IndexError:
                event_parameters = []

            if event_type == constants.BEAT_HIT:
                cur_beat = int(event_parameters[0])
                
                if 'sing' not in self.anim_prefix or self.animation.isFinished():
                    if cur_beat % 2 == 0:
                        if 'idle' in self.animations_dict:
                            self.play_animation('idle')
                        elif 'danceLeft' in self.animations_dict:
                            self.play_animation('danceLeft')
                    else:
                        if 'danceRight' in self.animations_dict and self.anim_prefix != 'cheer':
                            self.play_animation('danceRight')

            #ITS SO UGLYYYY. Maybe change this later? This might be the fastest way to do it.
            if event_type == constants.NOTE_BOT_PRESS:
                if not settings.settings['preferences']['two player']:
                    dir = int(event_parameters[1])

                    if (dir > 3 and self.character_type == 'opponent') or (dir <= 3 and self.character_type == 'player'):
                        pose = f'sing{constants.DIRECTIONS[dir % 4].upper()}'
                        self.play_animation(pose)

            if self.character_type == 'girlfriend': return

            if event_type in [constants.NOTE_GOOD_HIT, constants.NOTE_MISS]:
                pose = f'sing{constants.DIRECTIONS[int(event_parameters[1]) % 4].upper()}'
                if event_type == constants.NOTE_MISS: pose += 'miss'

                is_opponent = int(event_parameters[1]) > 3 and self.character_type == 'opponent'
                is_player = int(event_parameters[1]) <= 3 and self.character_type == 'player'

                if is_opponent or is_player: 
                    self.play_animation(pose)

    def tick(self, state):
        self.pos = (
            (self.screen_pos[0] - self.offsets_dict[self.anim_prefix][0] * 0.9 - state.camera_position_lerp[0]) + (state.zoomed_window_size[0] / 2) - constants.SCREEN_CENTER[0],
            (self.screen_pos[1] - self.offsets_dict[self.anim_prefix][1] * 0.9 - state.camera_position_lerp[1]) + (state.zoomed_window_size[1] / 2) - constants.SCREEN_CENTER[1]
        )

        self.animation.tickFrameNum()

    def draw(self, screen):
        self.animation.blit(screen, self.pos)