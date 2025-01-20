import json
from constants import *

#This file is mainly here to separate file saving logic for user settings.

def load_existing_settings():
    with open('settings.json', 'r+') as file:
        save_data = json.load(file)
    file.close()

    return save_data

def write_settings(settings_dict):
    with open('settings.json', 'w') as file:
        json.dump(settings_dict, file, indent = 4)
    file.close()

def load_settings():
    try:
        settings = load_existing_settings()
    except:
        settings = get_default_settings()
        write_settings(settings)
    
    return settings

def get_default_settings(): # If we cannot find a save file, use this to get default save data!
    settings = {
        #Edited in keybinds menu
        'keybinds': {
            'notes': None,

            'left': [pygame.K_a, pygame.K_LEFT],
            'down': [pygame.K_s, pygame.K_DOWN],
            'up': [pygame.K_w, pygame.K_UP],
            'right': [pygame.K_d, pygame.K_RIGHT],

            'ui': None,
            
            'menu_up': [pygame.K_w, pygame.K_UP],
            'menu_left': [pygame.K_a, pygame.K_LEFT],
            'menu_right': [pygame.K_d, pygame.K_RIGHT],
            'menu_down': [pygame.K_s, pygame.K_DOWN],

            'reset': [pygame.K_r, None],
            'forward': [pygame.K_RETURN, None],
            'back': [pygame.K_ESCAPE, None], 
            'pause': [pygame.K_p, None],

            'volume': None,

            'volume_up': [pygame.K_EQUALS, None],
            'volume_down': [pygame.K_MINUS, None],
            'volume_mute': [pygame.K_0, None]
        },

        #These are all in preferences menu.

        'preferences': {
            #Og game
            'naughtyness': True, #I don't know what this will ever do, but i'm adding it!
            'downscroll': False,
            'flashing lights': True,
            'camera zooming on beat': True,
            'debug display': False,
            'auto pause': True,
            'fps': 60, #Max frames per second.

            '': None,
            'Extra': None, #Value of none means it's just a visual object.

            'two player': False,
            'controller support': True,
            'debug freecam': False,
            'offset': 0,
        },
            
        'volume': 10 #Will go from 0 to 10; increments or decrements by 1.
    }
    return settings

#settings
settings = load_settings()
#print(settings)