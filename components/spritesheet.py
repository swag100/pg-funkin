import xml.etree.ElementTree as ET
import pygame
import xmltodict

from components.animation import Animation

class Spritesheet:
    def __init__(self, filename, scale = 1):
        self.filename = filename
        self.scale = scale

        self.subtexture_list = []

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        xml_path = filename.replace('png', 'xml')
        xml_data = ET.parse(xml_path).getroot()
        xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

        self.subtexture_list = dict(xmltodict.parse(xmlstr))['TextureAtlas']['SubTexture']
        
    def load_anim_frames(self, anim_name):
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
                'frameX': 0,
                'frameY': 0,
                'frameWidth': int(texture['@width']),
                'frameHeight': int(texture['@height'])
            }
            
            if any(anim in texture for anim in ['@frameX', '@frameY', '@frameWidth', '@frameHeight']):
                data['frameX'] = int(texture['@frameX']) * self.scale
                data['frameY'] = int(texture['@frameY']) * self.scale
                data['frameWidth'] = int(texture['@frameWidth'])
                data['frameHeight'] = int(texture['@frameHeight'])

            sprite = pygame.Surface((data['width'], data['height']), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(0, 0),(data['x'], data['y'], data['width'], data['height']))

            sprite_cut_frame = (0, 0, data['width'], data['height'])

            if '@rotated' in texture: #How many degrees? probably 90.
                sprite = pygame.transform.rotate(sprite, 90)
                sprite_cut_frame = (0, 0, data['height'], data['width']) #So sprites don't look cut off

            final_sprite = pygame.Surface((data['frameWidth'], data['frameHeight']), pygame.SRCALPHA)
            final_sprite.blit(sprite,(-data['frameX'], -data['frameY']), sprite_cut_frame)

            final_sprite = pygame.transform.smoothscale_by(final_sprite, self.scale)

            frame_data.insert(i, data)
            anim_frames.insert(i, final_sprite)
        
        return anim_frames
    
    def frames_to_animation(self, anim_frames):
        return Animation(anim_frames)
    
    def get_animation_names(self):
        return [str(self.subtexture_list[i]['@name'][:-4]) for i in range(len(self.subtexture_list))]

    def preload_animations(self):
        anim_dict = {}

        for texture_name in self.get_animation_names():
            if texture_name not in anim_dict:
                anim_dict[texture_name] = self.frames_to_animation(self.load_anim_frames(texture_name))

        self.animations = anim_dict