import pygame
import os

from random import randint

class Popup(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        self.image = image
        image_path = os.path.join('assets', 'images', 'ui', 'popup', f'{image}.png')

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, 0.6)
        self.rect = self.image.get_rect()
        self.alpha = 255 * 2

        self.rect.center = pos

        self.x_vel = randint(-10, 0)
        self.y_vel = -randint(1400, 1800)
        self.y_acc = randint(100, 140)
    def tick(self, dt):
        self.y_vel += self.y_acc

        self.alpha -= 20

        self.rect.center = (
            self.rect.center[0] + (self.x_vel * dt),
            self.rect.center[1] + ((self.y_vel / 10) * dt)
        )
    def draw(self, screen):
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)