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
    
    def tick(self, camera_position):
        for prop in self.props: prop.tick(camera_position)
    
    def draw(self, screen):
        for prop in self.props: prop.draw(screen)