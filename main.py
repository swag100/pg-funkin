import pygame
from states.playstate import PlayState
from game import Game

pygame.init()

pygame.display.set_caption('Rhythm')
screen = pygame.display.set_mode((1280, 720))

states = {
    'PlayState': PlayState()
}
game = Game(screen, states, 'PlayState')
game.run()