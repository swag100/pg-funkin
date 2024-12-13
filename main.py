import pygame
from spritesheet import Spritesheet



pygame.init()

screen = pygame.display.set_mode((480, 360))
pygame.display.set_caption('Rhythm')

screen.fill((255, 255, 255))

notes_sheet = Spritesheet('assets/images/noteStrumline.png')
note = notes_sheet.get_sprite('confirmHoldLeft0002')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(note, note.get_rect())
    pygame.display.flip()
    pygame.time.Clock().tick(60)