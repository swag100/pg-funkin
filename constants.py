import pygame

#This is a settings file, but ALSO a constants file... I'm just too lazy to separate it.

###CONSTANTS
WINDOW_TITLE = 'Rhythm'
WINDOW_SIZE = (1280, 720)

SCREEN_CENTER = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)

ANIM_FRAMERATE = 1 / 24

#gameplay constants
DIRECTIONS = ['left','down','up','right']

#hit windows, milliseconds
HIT_WINDOWS = {
    'perfect': 5,
    'killer': 12.5,
    'sick': 45,
    'good': 90,
    'bad': 135,
    'shit': 160
}

#health constants
HEALTH_MAX = 2
HEALTH_MIN = 0

HEALTH_STARTING = HEALTH_MAX / 2

HEALTH_BONUSES = {
    'perfect': 2 / 100 * HEALTH_MAX, #I think perfect and killer are the same
    'killer': 2 / 100 * HEALTH_MAX,
    'sick': 1.5 / 100 * HEALTH_MAX,
    'good': 0.75 / 100 * HEALTH_MAX,
    'bad': 0 / 100 * HEALTH_MAX,
    'shit': -1 / 100 * HEALTH_MAX,
    'holding': 7.5 / 100 * HEALTH_MAX #This one is per second.
}

HEALTH_PENALTIES = {
    'miss': 4 / 100 * HEALTH_MAX,
    'ghost miss': 2 / 100 * HEALTH_MAX, #No note there at all
    'hold miss': 0 / 100 * HEALTH_MAX #When you let go before the hold note is over.
}

#score constants
SCORE_BONUSES = {
    'sick': 350,
    'good': 200,
    'bad': 100,
    'shit': 50,
    'holding': 250 #Per second
}

#points to LOSE when you miss.
SCORE_PENALTY = 10 

#strum stuff
OPPONENT_STRUMLINE_OFFSET = (48, 24)
PLAYER_STRUMLINE_OFFSET = (676, 24)
STRUMLINE_SCALE_MULT = 0.7 #What to multiply anything related to strums by

SCROLL_SPEED_DIVISOR = 2

#event TYPES. Will be used BEFORE the slash (/) when posting an event.
BEAT_HIT = 'BEAT_HIT'

NOTE_GOOD_HIT = 'NOTE_GOOD_HIT'
NOTE_MISS = 'NOTE_MISS'
NOTE_BOT_PRESS = 'NOTE_BOT_PRESS'

SONG_BEGAN = 'SONG_BEGAN' #called when the countdown ends and the song's audio begins.
SONG_ENDED = 'SONG_ENDED' #Called when the conductor's song_position is greater than the length of the instrumental.

###SETTINGS DEFAULT VALUES to the user changing variables
SETTINGS_DEFAULT_VOLUME = 10 #Will go from 0 to 10; increments or decrements by 1
SETTINGS_DEFAULT_SONG_OFFSET = -120

SETTINGS_DEFAULT_FPS = 60 #Max frames per second.

SETTINGS_DEFAULT_RATING_POSITION = [500, 200]
SETTINGS_DEFAULT_COMBO_POSITION = [500, 280]

#keybinds
SETTINGS_DEFAULT_KEYBINDS = {
    'left': [pygame.K_a, pygame.K_LEFT],
    'down': [pygame.K_s, pygame.K_DOWN],
    'up': [pygame.K_w, pygame.K_UP],
    'right': [pygame.K_d, pygame.K_RIGHT],

    'menu_left': [pygame.K_a, pygame.K_LEFT],
    'menu_down': [pygame.K_s, pygame.K_DOWN],
    'menu_up': [pygame.K_w, pygame.K_UP],
    'menu_right': [pygame.K_d, pygame.K_RIGHT],

    'back': [pygame.K_ESCAPE], 
    'forward': [pygame.K_RETURN],
    'reset': [pygame.K_r],

    'volume': {
        'up': pygame.K_EQUALS, 
        'down': pygame.K_MINUS
    }
}

#Fun stuff
SETTINGS_DEFAULT_CAMERA_SPEED = 2