import pygame

###CONSTANTS
WINDOW_TITLE = 'Rhythm'
WINDOW_SIZE = (1280, 720)

DIRECTIONS = ['left','down','up','right']
SONG_OFFSET = 0

#strum positions
OPPONENT_STRUMLINE_OFFSET = (16, 24)
PLAYER_STRUMLINE_OFFSET = (700 - 24, 24)

#keybinds
KEYBINDS = {
    'left': [pygame.K_a, pygame.K_LEFT],
    'down': [pygame.K_s, pygame.K_DOWN],
    'up': [pygame.K_w, pygame.K_UP],
    'right': [pygame.K_d, pygame.K_RIGHT],

    'back': [pygame.K_ESCAPE], 
    'forward': [pygame.K_RETURN]
}

#events
BEAT_HIT = 'beat hit'

###variables
volume = 1 #Will go from 0 to 1; increments or decrements by 0.1