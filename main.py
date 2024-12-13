import pygame
from game import Game

game = Game()
while True:
    game.handle_events()
    game.tick()
    game.draw()