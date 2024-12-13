import sys
import pygame

class Game(object):
    def __init__(self, screen, states, initial_state):
        self.screen = screen
        self.states = states
        self.state_name = initial_state
        self.state = states[initial_state]

        self.clock = pygame.time.Clock()
        self.max_fps = 60

        self.done = False
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            self.state.handle_event(event)
    def set_state(self):
        next_state = self.state.next_state
        persistent_data = self.state.persistent_data

        #Set new state, pass persistent data
        self.state = self.states[next_state]
        self.state.start(persistent_data)
    def tick(self, dt):
        if self.state.done: self.set_state()
        self.state.tick(dt)
    def draw(self):
        self.state.draw(self.screen)
    def run(self):
        while not self.done:
            dt = self.clock.tick(self.max_fps) / 1000

            self.handle_events()
            self.tick(dt)
            self.draw()

            pygame.display.flip()