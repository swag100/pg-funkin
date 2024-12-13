import pygame
import xmltodict

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        with open(filename.replace('png', 'xml'), 'r') as file:  
            my_xml = file.read()
            self.subtextures = xmltodict.parse(my_xml)['TextureAtlas']['SubTexture']
        file.close()

    def load_animation(self, name): #Retrieve list of frames of animation from spritesheet
        animation = []
        for texture in self.subtextures:
            texture_name = texture['@name'][:-4]
            if name == texture_name:
                x, y, w, h = (
                    int(texture['@x']), 
                    int(texture['@y']), 
                    int(texture['@width']), 
                    int(texture['@height'])
                )

                sprite = pygame.Surface((w, h), pygame.SRCALPHA)
                sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
                animation.append(sprite)
        return animation