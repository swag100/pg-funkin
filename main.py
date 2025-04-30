import pygame
import constants
from game import Game

from states.mainmenustate import MainMenuState
from states.storymenustate import StoryMenuState
from states.freeplaystate import FreeplayMenuState
from states.playstate import PlayState
from states.gameoverstate import GameOverState
from states.optionstate import OptionsMenuState
from states.optionstate_preferences import OptionsPreferenceState
from states.optionstate_keybinds import OptionsKeyBindState

pygame.mixer.pre_init(44100, -16, 2, 64)
pygame.mixer.init()
pygame.joystick.init()
pygame.init()

pygame.mixer.set_num_channels(32) #So that spamming miss sounds satisfying

pygame.display.set_caption(constants.WINDOW_TITLE)
screen = pygame.display.set_mode(constants.WINDOW_SIZE, pygame.DOUBLEBUF)

states = {
    'MainMenuState': MainMenuState(),
    'StoryMenuState': StoryMenuState(),
    'FreeplayMenuState': FreeplayMenuState(),
    'PlayState': PlayState(),
    'GameOverState': GameOverState(),

    #Forgive me
    'OptionsMenuState': OptionsMenuState(),
    'OptionsPreferenceState': OptionsPreferenceState(),
    'OptionsKeyBindState': OptionsKeyBindState(),
}
game = Game(screen, states, 'MainMenuState')
game.run()