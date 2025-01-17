import os
import json
import pygame
import constants

#This file is mainly here to separate file saving logic for user settings.

def load_existing_settings():
    with open('settings.json', 'r+') as file:
        save_data = json.load(file)
    file.close()

    return save_data

def write_settings(settings_dict):
    with open('settings.json', 'w') as file:
        json.dump(settings_dict, file)
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
        'keybinds': constants.SETTINGS_DEFAULT_KEYBINDS,

        #These are all in preferences menu.

        #bools
        'naughtyness': constants.SETTINGS_DEFAULT_NAUGHTYNESS,
        'downscroll': constants.SETTINGS_DEFAULT_DOWNSCROLL,
        'autopause': constants.SETTINGS_DEFAULT_AUTO_PAUSE,
        '2player': constants.SETTINGS_DEFAULT_2PLAYER,
        'debug': constants.SETTINGS_DEFAULT_DEBUG_MODE,

        #the ones you press a or d on that make the number go bigger or smaller.
        'offset': constants.SETTINGS_DEFAULT_SONG_OFFSET,
        'fps': constants.SETTINGS_DEFAULT_FPS
    }
    return settings