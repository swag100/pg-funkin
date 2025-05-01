import pygame
import json

from components.prop import ColorProp, ImageProp, AnimatedProp

class Stage:
    def __init__(self, stage_name):
        self.stage = stage_name

        self.stage_data = self.load_stage_data()

        self.prop_data = self.stage_data['props']
        
        self.character_data = self.stage_data['characters']

        self.player_position = self.character_data['bf']['position']
        self.opponent_position = self.character_data['dad']['position']
        self.gf_position = self.character_data['gf']['position']
        
        self.player_cam_off = self.character_data['bf']['cameraOffsets']
        self.opponent_cam_off = self.character_data['dad']['cameraOffsets']
        self.gf_cam_off = self.character_data['gf']['cameraOffsets']

        self.cam_zoom = self.stage_data['cameraZoom']

        self.props = []
        for prop in self.prop_data:
            #self.props.insert(prop['zIndex'], Prop())
            
            #TODO: merge characters INTO stage class
            #   (basically make it so stage is IN CHARGE of drawing and updating characters, alongside props)
            #   all camgame stuff can be in the stage class, + zINDEX will WORK!

            if 'animations' in prop and len(prop['animations']) > 0:
                self.props.append(AnimatedProp(prop, 'stages/'))
            else:
                if '#' in prop['assetPath']: #Hashtags can be in filenames. Pick a better condition.
                    self.props.append(ColorProp(prop))
                else:
                    self.props.append(ImageProp(prop))

    def load_stage_data(self):
        stage_data_path = f'assets/data/stages/{self.stage}.json'
        with open(stage_data_path) as stage_data_file:
            stage_data = json.loads(stage_data_file.read())
        stage_data_file.close()

        return stage_data
    
    def on_beat_hit(self, cur_beat):
        for prop in self.props: 
            prop.on_beat_hit(cur_beat)
    
    def tick(self, camera_position, zoomed_window_size):
        for prop in self.props: prop.tick(camera_position, zoomed_window_size)
    
    def draw(self, screen):
        for prop in self.props: prop.draw(screen)