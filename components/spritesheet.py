import pygame
import xmltodict

class Spritesheet(pygame.sprite.Sprite):

    def __init__(self, filename, scale = 1):
        super().__init__()

        self.filename = filename

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        with open(filename.replace('png', 'xml'), 'r') as file:  
            my_xml = file.read()
            subtextures = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']
            self.animations = self.load_animations(subtextures, scale)
        file.close()


    def load_animations(self, subtextures, scale):
        animations_dict = {}
        for i in range(len(subtextures)):
            texture = subtextures[i]
            texture_name = str(texture['@name'][:-4])
            texture_id = int(texture['@name'][-4:])

            if texture_name not in animations_dict: 
                animations_dict[texture_name] = []

            x, y, w, h = (
                int(texture['@x']),
                int(texture['@y']),
                int(texture['@width']), 
                int(texture['@height'])
            )
            #int(texture['@frameX'])
            #int(texture['@frameY'])

            sprite = pygame.Surface((w, h), pygame.SRCALPHA)
            sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
            sprite = pygame.transform.smoothscale_by(sprite, scale)

            animations_dict[texture_name].insert(texture_id, sprite)
        print(animations_dict)
        return animations_dict