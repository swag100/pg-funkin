import pygame
from states.playstate import PlayState
from game import Game

pygame.mixer.pre_init(44100, -16, 2, 64)
pygame.mixer.init()
pygame.init()

pygame.display.set_caption('Rhythm')
screen = pygame.display.set_mode((1280, 720))

states = {
    'PlayState': PlayState()
}
game = Game(screen, states, 'PlayState')
game.run()