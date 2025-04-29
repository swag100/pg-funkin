import pygame

from components.spritesheet import Spritesheet

class Prop:
    def __init__(self, position, scroll = (1, 1)):
        self.position = position
        self.scroll_factor = scroll
        
    def on_beat_hit(self, cur_beat):
        pass

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

        self.image = pygame.image.load(path).convert_alpha()

        image_rect = self.image.get_rect()
        scale = prop_data['scale']

        self.image = pygame.transform.smoothscale(self.image, (image_rect.w * scale[0], image_rect.h * scale[1]))

class AnimatedProp(Prop):
    def __init__(self, prop_data, path_prefix = ''):
        self.prop_data = prop_data

        position = [0, 0]
        if 'position' in prop_data:
            position = prop_data['position']
        elif 'offsets' in prop_data:
            position = prop_data['offsets']
        scroll = [1, 1]
        if 'scroll' in prop_data:
            scroll = prop_data['scroll']

        Prop.__init__(self, position, scroll)

        path = 'assets/images/'+path_prefix+prop_data['assetPath']+'.png'

        if isinstance(prop_data['scale'], float):
            spritesheet = Spritesheet(path, prop_data['scale'])
        else:
            spritesheet = Spritesheet(path, prop_data['scale'][0])

        spritesheet.preload_animations()
        self.animations = spritesheet.animations

        start_animation = prop_data['animations'][0]['prefix']
        if 'startingAnimation' in prop_data:
            start_animation = prop_data['startingAnimation']

        self.dance_every = 0
        if 'danceEvery' in prop_data:
            self.dance_every = prop_data['danceEvery']
        
        """
        if 'name' in prop_data:
            print(prop_data['name'], start_animation)

            print(prop_data['animations'])
            print(self.animations)
        """
            
        self.animation = self.animations[start_animation]

        anim_names = list(self.animations.keys()) #easier to read

        #this code is disgusting. I might clean it up later. But it works!
        try:
            self.animation.play(loop=prop_data['animations'][anim_names.index(start_animation)]['looped'])
        except:
            self.animation.play()

    
    def on_beat_hit(self, cur_beat):
        if self.dance_every > 0:
            if cur_beat % 2 == 0: #TODO: make proportional to self.dance_every
                if 'idle' in self.animations:
                    self.play_animation('idle')
                elif 'danceLeft' in self.animations:
                    self.play_animation('danceLeft')
            else:
                if 'danceRight' in self.animations:
                    self.play_animation('danceRight')

    def tick(self, camera_position = [0, 0]): #Update position based on scroll factor
        super().tick(camera_position)
        self.animation.tickFrameNum()

    def play_animation(self, prefix, loop = False, start_time = None):
        self.animation.stop()

        self.anim_prefix = prefix
        self.animation = self.animations[prefix]

        self.animation.play(loop, start_time)

    def draw(self, screen):
        self.animation.blit(screen, self.scrolled_position)