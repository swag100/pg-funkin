import pygame
import json

from components.spritesheet import Spritesheet

class Prop:
    def __init__(self, position, scroll = (1, 1)):
        self.position = position
        self.scroll_factor = scroll

    def tick(self, camera_position): #Update position based on scroll factor
        self.scrolled_position = (
            (self.position[0] - camera_position[0]) * self.scroll_factor[0],
            (self.position[1] - camera_position[1]) * self.scroll_factor[1]
        )
    
    def draw(self, screen):
        screen.blit(self.image, self.scrolled_position)

class ImageProp(Prop):
    def __init__(self, prop_data):
        Prop.__init__(self, prop_data['position'], prop_data['scroll'])

        path = 'assets/images/stages/'+prop_data['assetPath']+'.png'
        print(path)

        self.image = pygame.image.load(path).convert_alpha()

        image_rect = self.image.get_rect()
        scale = prop_data['scale']

        self.image = pygame.transform.smoothscale(self.image, (image_rect.w * scale[0], image_rect.h * scale[1]))

class AnimatedProp(Prop):
    def __init__(self, prop_data):
        Prop.__init__(self, prop_data['position'], prop_data['scroll'])

        path = 'assets/images/stages/'+prop_data['assetPath']+'.png'
        spritesheet = Spritesheet(path, prop_data['scale'][0])
        spritesheet.preload_animations()
        self.animations = spritesheet.animations

        self.animation = self.animations[prop_data['animations'][0]['prefix']]
        self.animation.play()

    def draw(self, screen):
        self.animation.blit(screen, self.scrolled_position)

"""
self.props.insert(prop['zIndex'], Prop(
        prop['assetPath'], 
        prop['position'], 
        prop['animations'], 
        prop['scroll'], 
        prop['scale']
    )
)
"""

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

        self.cam_zoom = self.stage_data['cameraZoom']

        self.props = []
        for prop in self.prop_data:
            try:
                if 'animations' in prop and len(prop['animations']) > 0:
                    self.props.insert(prop['zIndex'], AnimatedProp(prop))
                else:
                    self.props.insert(prop['zIndex'], ImageProp(prop))
            except FileNotFoundError:
                pass

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