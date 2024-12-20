import pygame
import os

#Simple class for countdown images.

class Countdown(pygame.sprite.Sprite):
    def __init__(self, image, pos, scale = 0.8):
        self.image = image
        image_path = os.path.join('assets', 'images', 'ui', 'countdown', f'{image}.png')

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, scale)
        self.rect = self.image.get_rect(center = pos)

        self.alpha = 255 * 1.8

    def tick(self, dt):
        self.alpha -= 1400 * dt

    def draw(self, screen):
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)