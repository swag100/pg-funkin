import pygame
import xmltodict
import components.pyganim as pyganim

class Spritesheet:
    def __init__(self, filename, scale = 1):
        self.filename = filename

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        with open(filename.replace('png', 'xml'), 'r') as file:  
            my_xml = file.read()
            subtextures = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']
            self.animations = self.load_animations(subtextures, scale)
        file.close()

    def load_animations(self, subtextures, scale):
        frame_data = {}
        animations = {}
        for i in range(len(subtextures)):
            texture = subtextures[i]
            texture_name = str(texture['@name'][:-4])
            texture_index = int(texture['@name'][-4:])

            if texture_name not in frame_data: 
                frame_data[texture_name] = []
                animations[texture_name] = []
            
            data = {
                'x': int(texture['@x']),
                'y': int(texture['@y']),
                'width': int(texture['@width']),
                'height': int(texture['@height']),
                'frameX': int(texture['@frameX']) * scale, 
                'frameY': int(texture['@frameY']) * scale,
                'frameWidth': int(texture['@frameWidth']), 
                'frameHeight': int(texture['@frameHeight'])
            }

            sprite = pygame.Surface((data['frameWidth'], data['frameHeight']), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(-data['frameX'], -data['frameY']),(data['x'], data['y'], data['width'], data['height']))
            sprite = pygame.transform.smoothscale_by(sprite, scale)

            frame_data[texture_name] = data
            animations[texture_name].insert(texture_index, sprite)

        #Finally, convert animations into a dict of Animation objects
        animation_objects = {}
        for key, value in animations.items():
            animation_objects[key] = pyganim.Animation(value)
        
        return animation_objects