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
        'keybinds': SETTINGS_DEFAULT_KEYBINDS,

        #These are all in preferences menu.

        'preferences': {
            #Og game
            'naughtyness': SETTINGS_DEFAULT_NAUGHTYNESS,
            'downscroll': SETTINGS_DEFAULT_DOWNSCROLL,
            'flashing lights': SETTINGS_DEFAULT_FLASHING_LIGHTS,
            'camera zooming on beat': SETTINGS_DEFAULT_CAMERA_ZOOMING_ON_BEAT,
            'debug display': SETTINGS_DEFAULT_DEBUG_MODE,
            'auto pause': SETTINGS_DEFAULT_AUTO_PAUSE,
            'fps': SETTINGS_DEFAULT_FPS,

            '': None,
            'Extra': None, #Value of none means it's just a visual object.

            'debug freecam': SETTINGS_DEFAULT_DEBUG_FREECAM,
            'two player': SETTINGS_DEFAULT_2PLAYER,
            'offset': SETTINGS_DEFAULT_SONG_OFFSET,
        },
            
        'volume': SETTINGS_DEFAULT_VOLUME
    }
    return settings

#settings
settings = load_settings()
#print(settings)