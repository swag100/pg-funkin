class BaseState:
    def __init__(self):
        self.next_state = None
        self.done = False

    def start(self, persistent_data): 
        self.persistent_data = persistent_data

    def handle_event(self, event): 
        pass

    def tick(self, dt): 
        pass

    def draw(self, screen): 
        pass