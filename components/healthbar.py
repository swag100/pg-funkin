import pygame
import os

class BarIcon:
    def __init__(self, play_state, character, player = False, size = 150):
        self.play_state = play_state
        self.health_bar = play_state.health_bar
        self.player = player

        image_path = os.path.join('assets', 'images', 'ui', 'icons', f'icon-{character}.png')
        self.images = self.seperate_images(image_path, size, player)

        self.image = self.images[0] #0: normal, 1: hurt
        self.rect = self.image.get_rect()

        self.bump_size = 1.15
        self.size = self.bump_size
    
    def seperate_images(self, image_path, size, flipped):
        sheet = pygame.image.load(image_path)
        sheet_rect = sheet.get_rect()

        images = []

        for i in range(int(sheet_rect.w / size)):
            image = pygame.Surface.subsurface(sheet, pygame.Rect(i * size, 0, size, size))
            image = pygame.transform.flip(image, flipped, False)
            images.append(image)
        
        return images
    
    def tick(self, dt):
        self.image = self.images[int(self.play_state.health <= 0.4)]
        self.size += (1 - self.size) / 8

        x_offset = (self.play_state.health_lerp / 2) * (self.health_bar.image_rect.w - 8) - (self.health_bar.image_rect.w / 2)
        
        self.rect.center = self.health_bar.lower_bar.center
        self.rect.centerx -= x_offset


    def draw(self, screen):
        scaled_image = pygame.transform.smoothscale_by(self.image, self.size)

        if self.player:
            scaled_image_rect = scaled_image.get_rect(left = self.rect.centerx - 20, centery = self.rect.centery)
        else:
            scaled_image_rect = scaled_image.get_rect(right = self.rect.centerx + 20, centery = self.rect.centery)



        screen.blit(scaled_image, scaled_image_rect)

    def bump(self):
        self.size = self.bump_size


class HealthBar:
    def __init__(self, play_state, pos):
        self.play_state = play_state

        image_path = os.path.join('assets', 'images', 'ui', 'healthbar.png')

        self.image = pygame.image.load(image_path)

        self.image_rect = self.image.get_rect()
        self.pos = (pos[0] - (self.image_rect.w / 2), pos[1] - (self.image_rect.h / 2))

        self.lower_bar = pygame.Rect(
            self.pos[0] + self.image_rect.x + 4,
            self.pos[1] + self.image_rect.y + 4,
            self.image_rect.w - 8,
            self.image_rect.h - 8
        )
        self.upper_bar = pygame.Rect(
            self.pos[0] + self.image_rect.x + 4,
            self.pos[1] + self.image_rect.y + 4,
            (self.image_rect.w - 8) * self.play_state.health,
            self.image_rect.h - 8
        ) #This bar goes over lowerbar; it's the green one that shows health.

    def tick(self, dt):
        self.upper_bar.w = (self.image_rect.w - 8) * (self.play_state.health_lerp / 2)
        self.upper_bar.right = self.lower_bar.right

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        pygame.draw.rect(screen, (255, 0, 0), self.lower_bar)
        pygame.draw.rect(screen, (0, 255, 0), self.upper_bar)