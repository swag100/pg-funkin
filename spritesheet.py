import pygame
import xmltodict

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        with open(filename.replace('png', 'xml'), 'r') as file:  
            my_xml = file.read()
            self.subtextures = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']

            for texture in self.subtextures: print(texture)
        file.close()

    def get_sprite(self, name): #Retrieve sprite from spritesheet
        for texture in self.subtextures:
            if name == texture['@name']:
                x, y = int(texture['@x']), int(texture['@y'])
                w, h = int(texture['@width']), int(texture['@height'])
                sprite = pygame.Surface((w, h))
                sprite.set_colorkey((0,0,0))
                sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
                return sprite