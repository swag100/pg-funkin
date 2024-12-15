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
        self.frame_data = {}
        animations = {}
        animation_objects = {}
        for i in range(len(subtextures)):
            texture = subtextures[i]
            texture_name = str(texture['@name'][:-4])
            texture_index = int(texture['@name'][-4:])

            if texture_name not in self.frame_data: 
                self.frame_data[texture_name] = []
                animations[texture_name] = []
            
            data = {
                'x': int(texture['@x']),
                'y': int(texture['@y']),
                'width': int(texture['@width']),
                'height': int(texture['@height']),
                'frameX': -int(texture['@frameX']) * scale, 
                'frameY': -int(texture['@frameY']) * scale
            }

            sprite = pygame.Surface((data['width'], data['height']), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(0, 0),(data['x'], data['y'], data['width'], data['height']))
            sprite = pygame.transform.smoothscale_by(sprite, scale)

            self.frame_data[texture_name] = data
            animations[texture_name].insert(texture_index, sprite)

        #Clean this up too, please
        for key, value in animations.items():
            animation_objects[key] = pyganim.Animation(value)
        return animation_objects
    def draw(self, screen, dest):
        #THIS HAS THE WRONG POSITIONS i think; FIX NOW
        for texture_name in self.animations.keys():
            dest = (
                dest[0] + self.frame_data[texture_name]['frameX'], 
                dest[1] + self.frame_data[texture_name]['frameY']
            )

            self.animations[texture_name].blit(screen, dest)