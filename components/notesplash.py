from random import randint
from components.spritesheet import Spritesheet

class NoteSplash:
    def __init__(self, strumline):
        self.strumline = strumline
        self.direction = self.strumline.id % 4

        rand_anim = randint(0, 1) + 1
        peak = ['purple', 'blue', 'green', 'red']
        if rand_anim == 1: peak[1] = ' blue'

        spritesheet = Spritesheet('assets/images/noteSplashes.png', 0.9)
        anim_frames = spritesheet.load_animation(f'note impact {rand_anim} {peak[self.direction]}')

        self.animation = spritesheet.frames_to_animation(anim_frames)
        self.animation.set_alpha(255 * 0.6)

        self.rect = self.animation.getCurrentFrame().get_rect()
        self.rect.centerx = self.strumline.strum_note.position('static')[0] + 77
        self.rect.centery = self.strumline.strum_note.position('static')[1] + 72


        self.animation.play()

    def draw(self, screen):

        self.animation.blit(screen, self.rect)
        #pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 20)