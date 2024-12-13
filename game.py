import pygame
from spritesheet import Spritesheet

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Rhythm')


class Game:
    def __init__(self):
        #Make sprite group instead of just a list to contain game objects
        self.press = 'down'
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    def tick(self):
        
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]: self.press = 'right'
        if keys[K_LEFT]: self.press = 'left'
        if keys[K_UP]: self.press = 'up'
        if keys[K_DOWN]: self.press = 'down'

        notes_sheet = Spritesheet('assets/images/noteStrumline.png')
        self.note = notes_sheet.load_animation('static'+self.press)[0]

        pygame.time.Clock().tick(60)
    def draw(self):
        screen.fill((255, 255, 255))
        
        screen.blit(self.note, self.note.get_rect())

        pygame.display.flip()