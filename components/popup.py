import pygame
import os

from random import randint

class Popup(pygame.sprite.Sprite):
    def __init__(self, image, pos, scale = 0.6, i = 0):
        self.image = image
        image_path = os.path.join('assets', 'images', 'ui', 'popup', f'{image}.png')

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, scale)
        self.rect = self.image.get_rect()

        self.alpha = 255 * 2

        self.rect.centerx = pos[0] + (i * self.rect.w) + 16
        self.rect.centery = pos[1]

        self.x_vel = randint(-10, 0)
        self.y_vel = -randint(1400, 1800)
        self.y_acc = randint(100, 140)

    def tick(self, dt):
        self.y_vel += self.y_acc

        self.alpha -= 20

        self.rect.centerx += self.x_vel * dt
        self.rect.centery += (self.y_vel / 10) * dt

    def draw(self, screen):
        self.image.set_alpha(self.alpha)
        screen.blit(self.image, self.rect)