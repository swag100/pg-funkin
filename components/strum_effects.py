from random import randint
from components.spritesheet import Spritesheet

note_colors = ['purple', 'blue', 'green', 'red']

class NoteSplash:
    def __init__(self, strumline):
        self.strumline = strumline
        self.direction = self.strumline.id % 4

        rand_anim = randint(0, 1) + 1
        peak = note_colors.copy()
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

class HoldCover:
    def __init__(self, sustain):
        self.sustain = sustain
        self.direction = sustain.id
        self.color = note_colors[self.direction]

        self.spritesheet = Spritesheet(f'assets/images/holdCover{self.color.title()}.png', 0.9)
        self.spritesheet.preload_animations()
        self.animation = self.spritesheet.animations[f'holdCoverStart{self.color.title()}']

        self.anim_timer = 0

        self.animation.play()

    def tick(self, dt):
        self.anim_timer += dt

        self.rect = self.animation.getCurrentFrame().get_rect()
        self.rect.centerx = self.sustain.note.strumline.strum_note.position('static')[0] + 71
        self.rect.centery = self.sustain.y + 53

        if self.anim_timer >= 2 / 24:
            self.animation = self.spritesheet.animations[f'holdCover{self.color.title()}']
            self.animation.play(True)

    def draw(self, screen):
        self.animation.blit(screen, self.rect)
        #pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 20)

class ReleaseSplash:
    def __init__(self, strumline):
        self.strumline = strumline
        self.direction = self.strumline.id % 4
        self.color = note_colors[self.direction]

        spritesheet = Spritesheet(f'assets/images/holdCover{self.color.title()}.png')

        anim_frames = spritesheet.load_animation(f'holdCoverEnd{self.color.title()}')
        self.animation = spritesheet.frames_to_animation(anim_frames)

        self.rect = self.animation.getCurrentFrame().get_rect()
        self.rect.centerx = self.strumline.strum_note.position('static')[0] + 57
        self.rect.centery = self.strumline.strum_note.position('static')[1] + 132

        self.animation.play()

    def draw(self, screen):
        self.animation.blit(screen, self.rect)
        #pygame.draw.circle(screen, (255, 0, 0), self.rect.center, 20)