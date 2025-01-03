import sys
import constants
import pygame

class Game(object):
    def __init__(self, screen, states, initial_state):
        self.screen = screen
        self.states = states
        self.state_name = initial_state
        self.state = states[initial_state]

        self.state.start({})

        self.clock = pygame.time.Clock()
        self.max_fps = constants.SETTINGS_DEFAULT_FPS

        self.done = False

        #Volume GUI
        self.volume_rect = pygame.Rect(constants.SCREEN_CENTER[0] - 80, -60, 160, 60)
        self.volume_surface = pygame.Surface((160,60), pygame.SRCALPHA)
        self.volume_visible_time = 0 #Seconds that volume GUI is visible.
        
        volume_font = pygame.font.Font('assets/fonts/nokiafc22.ttf', 20)
        self.volume_text = volume_font.render('VOLUME', True, (255, 255, 255))

        self.fps_font = pygame.font.Font('assets/fonts/arial.ttf', 10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == constants.SETTINGS_DEFAULT_KEYBINDS['volume']['down']:
                    if constants.SETTINGS_DEFAULT_VOLUME - 1 >= 0:
                        constants.SETTINGS_DEFAULT_VOLUME -= 1
                if event.key == constants.SETTINGS_DEFAULT_KEYBINDS['volume']['up']:
                    if constants.SETTINGS_DEFAULT_VOLUME + 1 <= 10:
                        constants.SETTINGS_DEFAULT_VOLUME += 1
                
                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['volume'].values():
                    self.volume_visible_time
                    self.volume_rect.y = 0

                    volume_noise = pygame.mixer.Sound('assets/sounds/volume.ogg')
                    volume_noise.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                    volume_noise.play()

            self.state.handle_event(event)
    def set_state(self):
        next_state = self.state.next_state
        persistent_data = self.state.persistent_data

        #Set new state, pass persistent data
        if next_state in self.states.keys():
            self.state = self.states[next_state]
        else:
            print(f'Failed to find {next_state}. Reloading state')
        self.state.start(persistent_data)
    def tick(self, dt):
        if self.state.done: self.set_state()
        self.state.tick(dt)

        #volume graphic
        if self.volume_rect.y == 0:
            self.volume_visible_time += dt
        if self.volume_visible_time >= 1:
            if self.volume_rect.y - 20 >= -60:
                self.volume_rect.y -= 20
            else:
                self.volume_visible_time = 0
        #fps counter
        fps = int(self.clock.get_fps())
        self.fps_text = self.fps_font.render(f'FPS: {fps}', True, (255, 255, 255))

    def draw(self):
        self.state.draw(self.screen)

        #Volume
        self.volume_surface.fill((0,0,0,128))
        self.screen.blit(self.volume_surface, self.volume_rect)
        for i in range(10):
            rect = pygame.Rect(i * 12 + 20, 0, 8, (i + 1) * 2)
            rect.bottom = 30
            surface = pygame.Surface((rect.w,rect.h), pygame.SRCALPHA)
            surface.fill((255,255,255,128))
            self.screen.blit(surface, (rect.x + self.volume_rect.x, rect.y + self.volume_rect.y))
        for i in range(constants.SETTINGS_DEFAULT_VOLUME):
            rect = pygame.Rect(i * 12 + 20, 0, 8, (i + 1) * 2)
            rect.bottom = 30
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(rect.x + self.volume_rect.x, rect.y + self.volume_rect.y, rect.w, rect.h))
        self.screen.blit(self.volume_text, (self.volume_rect.x + 30, self.volume_rect.y + 34))
        self.screen.blit(self.fps_text, (6, 2))

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.max_fps) / 1000

            self.handle_events()
            self.tick(dt)
            self.draw()

            pygame.display.flip()