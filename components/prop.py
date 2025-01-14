import pygame

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

class ColorProp(Prop):
    def __init__(self, prop_data):
        Prop.__init__(self, prop_data['position'], prop_data['scroll'])

        color = pygame.Color(prop_data['assetPath'])

        self.color = (color[0], color[1], color[2])
        self.scale = prop_data['scale']
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(*self.scrolled_position, *self.scale))

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
        position = [0, 0]
        if 'position' in prop_data:
            position = prop_data['position']
        elif 'offsets' in prop_data:
            position = prop_data['offsets']
        scroll = [1, 1]
        if 'scroll' in prop_data:
            scroll = prop_data['scroll']

        Prop.__init__(self, position, scroll)

        path = 'assets/images/stages/'+prop_data['assetPath']+'.png'

        if isinstance(prop_data['scale'], float):
            spritesheet = Spritesheet(path, prop_data['scale'])
        else:
            spritesheet = Spritesheet(path, prop_data['scale'][0])

        spritesheet.preload_animations()
        self.animations = spritesheet.animations

        self.animation = self.animations[prop_data['animations'][0]['prefix']]
        self.animation.play()

    def tick(self, camera_position): #Update position based on scroll factor
        self.scrolled_position = (
            (self.position[0] - camera_position[0]) * self.scroll_factor[0],
            (self.position[1] - camera_position[1]) * self.scroll_factor[1]
        )
        self.animation.tickFrameNum()

    def play_animation(self, prefix, loop = False, start_time = None):
        self.animation.stop()

        self.anim_prefix = prefix
        self.animation = self.animations_dict[prefix]

        self.animation.play(loop, start_time)

    def draw(self, screen):
        self.animation.blit(screen, self.scrolled_position)