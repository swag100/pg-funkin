import json
from .basestate import BaseState

#EXTREMELY simple state; only meant for transferring week info to the playstate for now.

class StoryMenuState(BaseState):
    def __init__(self):
        super(StoryMenuState, self).__init__()
        
        self.level_data = self.load_level_data('week1') #TODO: make it so user can pick a level + difficulty. Requires making the GUI
        self.level_songs = self.level_data['songs']

    def load_level_data(self, level):
        level_path = f'assets/data/levels/{level}.json'
        with open(level_path) as level_data_file:
            level_data = json.loads(level_data_file.read())
        level_data_file.close()

        return level_data

    def start(self, persistent_data): 
        self.persistent_data = persistent_data

        self.persistent_data['songs'] = self.level_songs
        self.persistent_data['difficulty'] = 'hard' #TODO: Please, make this variable later..
        
        self.next_state = 'PlayState' #Load playstate, make sure to give it the persistant data of the week.
        self.done = True