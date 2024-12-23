import pygame
import constants
from game import Game

from states.storymenustate import StoryMenuState
from states.playstate import PlayState

pygame.mixer.pre_init(44100, -16, 2, 64)
pygame.mixer.init()
pygame.init()

pygame.display.set_caption(constants.WINDOW_TITLE)
screen = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.DOUBLEBUF, 16)

states = {
    'StoryMenuState': StoryMenuState(),
    'PlayState': PlayState()
}
game = Game(screen, states, 'StoryMenuState')
game.run()