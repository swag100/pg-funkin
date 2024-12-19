import pygame
import xmltodict

from components.animation import Animation

class Spritesheet:
    def __init__(self, filename, scale = 1):
        self.filename = filename
        self.scale = scale

        self.subtexture_list = []

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        with open(filename.replace('png', 'xml'), 'r', encoding='utf-8-sig') as file:  
            my_xml = file.read()
            self.subtexture_list = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']
            #self.preload_animations(self.subtexture_data, scale) #job for the people using this class
        file.close()
    
    def load_animation(self, anim_name):
        subtextures = [i for i in self.subtexture_list if anim_name == i['@name'][:-4]]

        frame_data = []
        anim_frames = []
        for i in range(len(subtextures)):
            texture = subtextures[i]
            
            data = {
                'x': int(texture['@x']),
                'y': int(texture['@y']),
                'width': int(texture['@width']),
                'height': int(texture['@height']),

                #these mirror x, y, width, height. Will be overwritten if file actually has these
                'frameX': int(texture['@x']),
                'frameY': int(texture['@y']),
                'frameWidth': int(texture['@width']),
                'frameHeight': int(texture['@height'])
            }
            
            if any(anim in texture for anim in ['@frameX', '@frameY', '@frameWidth', '@frameHeight']):
                data['frameX'] = int(texture['@frameX']) * self.scale
                data['frameY'] = int(texture['@frameY']) * self.scale
                data['frameWidth'] = int(texture['@frameWidth'])
                data['frameHeight'] = int(texture['@frameHeight'])

            sprite = pygame.Surface((data['frameWidth'], data['frameHeight']), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(-data['frameX'], -data['frameY']),(data['x'], data['y'], data['width'], data['height']))
            sprite = pygame.transform.smoothscale_by(sprite, self.scale)

            frame_data.insert(i, data)
            anim_frames.insert(i, sprite)
        
        return anim_frames
    
    def frames_to_animation(self, anim_frames):
        return Animation(anim_frames)

    def preload_animations(self):
        anim_dict = {}

        for i in range(len(self.subtexture_list)):
            texture_name = str(self.subtexture_list[i]['@name'][:-4])

            if texture_name not in anim_dict:
                anim_dict[texture_name] = self.frames_to_animation(self.load_animation(texture_name))

        self.animations = anim_dict