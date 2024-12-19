import pygame

###CONSTANTS
WINDOW_TITLE = 'Rhythm'
WINDOW_SIZE = (1280, 720)

DIRECTIONS = ['left','down','up','right']
SONG_OFFSET = 0

ANIM_FRAMERATE = 1/24

SCROLL_SPEED_DIVISOR = 2

#strum positions
STRUMLINE_SCALE_MULT = 0.7 #What to multiply anything related to strums by
OPPONENT_STRUMLINE_OFFSET = (16, 24)
PLAYER_STRUMLINE_OFFSET = (700 - 24, 24)

#hit windows, milliseconds
HIT_WINDOWS = {
    'sick': 45,
    'good': 90,
    'bad': 135,
    'shit': 160
}

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