import pygame
import json

class Prop:
    def __init__(self, image_path, position, scroll = (1, 1), scale = (1, 1)):
        self.image = pygame.image.load(f'assets/images/{image_path}.png')
        self.position = position
        self.scroll_factor = scroll

        image_rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (image_rect.w * scale[0], image_rect.h * scale[1]))

    def tick(self, dt, camera_position): #Update position based on scroll factor
        self.scrolled_position = (
            (self.position[0] - camera_position[0]) * self.scroll_factor[0],
            (self.position[1] - camera_position[1]) * self.scroll_factor[1]
        )
    
    def draw(self, screen):
        screen.blit(self.image, self.scrolled_position)

"""
"position": [-600, -200],
"scale": [1, 1],
"assetPath": "stageback",
"scroll": [0.9, 0.9],
"""

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

        print(self.character_data)

        self.cam_zoom = self.stage_data['cameraZoom']

        self.props = []
        for prop in self.prop_data:
            self.props.insert(prop['zIndex'], Prop(prop['assetPath'], prop['position'], prop['scroll'], prop['scale']))

    def load_stage_data(self):
        stage_data_path = f'assets/data/stages/{self.stage}.json'
        with open(stage_data_path) as stage_data_file:
            stage_data = json.loads(stage_data_file.read())
        stage_data_file.close()

        return stage_data
    
    def tick(self, dt, camera_position):
        for prop in self.props: prop.tick(dt, camera_position)
    
    def draw(self, screen):
        for prop in self.props: prop.draw(screen)