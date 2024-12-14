import pygame
import xmltodict

class Spritesheet:

    def __init__(self, filename):
        self.filename = filename

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        with open(filename.replace('png', 'xml'), 'r') as file:  
            my_xml = file.read()
            subtextures = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']
            self.animations = self.load_animations(subtextures)
        file.close()


    def load_animations(self, subtextures):
        animations_dict = {}
        anim_frames = []
        old_texture_name = ''
        for i in range(len(subtextures)):

            texture = subtextures[i]
            texture_name = str(texture['@name'][:-4])
            texture_id = int(texture['@name'][-4:])

            x, y, w, h = (
                int(texture['@x']), # + int(texture['@frameX'])
                int(texture['@y']), # + int(texture['@frameY'])
                int(texture['@width']), 
                int(texture['@height'])
            )

            sprite = pygame.Surface((w, h), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
            anim_frames.insert(texture_id, sprite)
            
            if old_texture_name != texture_name: #This is a new texture
                old_texture_name = texture_name
                animations_dict[texture_name] = anim_frames
                anim_frames = []
        #All animations are completely offset; fix now
        print(animations_dict)
        return animations_dict