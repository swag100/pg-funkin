import sys
import constants
import pygame
from settings import *

class Game(object):
    def __init__(self, screen, states, initial_state):
        self.screen = screen
        self.states = states
        self.state_name = initial_state
        self.state = states[initial_state]

        #window
        self.focused = True

        #Controller vars
        self.joysticks = self.get_joysticks()
        self.hat_pressed = [0, 0] #I hate this "hat" thing.

        #Volume GUI
        self.volume_rect = pygame.Rect(constants.SCREEN_CENTER[0] - 80, -60, 160, 60)
        self.volume_surface = pygame.Surface((160,60), pygame.SRCALPHA)
        self.volume_visible_time = 0 #Seconds that volume GUI is visible.
        
        volume_font = pygame.font.Font('assets/fonts/nokiafc22.ttf', 20)
        self.volume_text = volume_font.render('VOLUME', True, (255, 255, 255))

        self.fps_font = pygame.font.Font('assets/fonts/arial.ttf', 10)

        #Finally, start state!
        self.state.start({'game': self})

        self.clock = pygame.time.Clock()

        self.done = False

    def get_joysticks(self):
        return [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #print(event)

            #Window focus events.
            if settings['preferences']['auto pause']:
                if event.type == pygame.WINDOWFOCUSGAINED:
                    self.focused = True
                    if hasattr(self.state, 'paused') and self.state.paused:
                        return
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
                if event.type == pygame.WINDOWFOCUSLOST:
                    self.focused = False
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()

            #Controller things :)
            if settings['preferences']['controller support']:
                if event.type == pygame.JOYDEVICEADDED:
                    self.joysticks = self.get_joysticks()
                    for joystick in self.joysticks:
                        print(joystick.get_name())
                if event.type == pygame.JOYDEVICEREMOVED:
                    self.joysticks = self.get_joysticks()

                #convert button press to key down. Sorry liberals!
                if event.type == pygame.JOYHATMOTION:
                    #print(event.joy, event.joy %2)
                    x, y = event.value

                    #This took longer than I'd like to admit.
                    event_type = pygame.KEYDOWN

                    if x != self.hat_pressed[0]:
                        if self.hat_pressed[0] > 0 or x > 0: 
                            simulated_key = settings['keybinds']['right'][event.joy % 2]
                        elif self.hat_pressed[0] < 0 or x < 0: 
                            simulated_key = settings['keybinds']['left'][event.joy % 2]

                        if x == 0: 
                            event_type = pygame.KEYUP
                        
                        self.hat_pressed[0] = x

                    if y != self.hat_pressed[1]:
                        if self.hat_pressed[1] > 0 or y > 0: 
                            simulated_key = settings['keybinds']['up'][event.joy % 2]
                        elif self.hat_pressed[1] < 0 or y < 0: 
                            simulated_key = settings['keybinds']['down'][event.joy % 2]
                            
                        if y == 0: 
                            event_type = pygame.KEYUP

                        self.hat_pressed[1] = y


                    event = pygame.event.Event(event_type, key = simulated_key)

                if self.state_name == 'PlayState' and not self.state.paused: #Hardcoded? Sorry!
                    if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
                        simulated_key = None

                        if event.button == pygame.CONTROLLER_BUTTON_A:
                            simulated_key = settings['keybinds']['down'][event.joy % 2]
                        if event.button == pygame.CONTROLLER_BUTTON_B:
                            simulated_key = settings['keybinds']['right'][event.joy % 2]
                        if event.button == pygame.CONTROLLER_BUTTON_X:
                            simulated_key = settings['keybinds']['left'][event.joy % 2]
                        if event.button == pygame.CONTROLLER_BUTTON_Y:
                            simulated_key = settings['keybinds']['up'][event.joy % 2]

                        event_type = pygame.KEYUP if event.type == pygame.JOYBUTTONUP else pygame.KEYDOWN

                        if simulated_key != None:
                            event = pygame.event.Event(event_type, key=simulated_key)
                else:
                    if event.type == pygame.JOYBUTTONDOWN:
                        simulated_key = None
                        
                        if event.button == pygame.CONTROLLER_BUTTON_A:
                            simulated_key = settings['keybinds']['forward'][0]
                        if event.button == pygame.CONTROLLER_BUTTON_B:
                            simulated_key = settings['keybinds']['back'][0]

                        if simulated_key != None:
                            event = pygame.event.Event(pygame.KEYDOWN, key=simulated_key)
                if event.type == pygame.JOYBUTTONDOWN:
                    simulated_key = None
                    
                    if event.button == 7: #On a dualshock 3, this is start. Might conflict with other controllers.
                        simulated_key = settings['keybinds']['forward'][0]
                    if event.button == pygame.CONTROLLER_BUTTON_START: #select on dualshock3
                        simulated_key = settings['keybinds']['back'][0]

                    if simulated_key != None:
                        event = pygame.event.Event(pygame.KEYDOWN, key=simulated_key)
            ######### end of controller code

            if event.type == pygame.KEYDOWN:
                if event.key in settings['keybinds']['volume_down']:
                    if settings['volume'] - 1 >= 0: settings['volume'] -= 1
                if event.key in settings['keybinds']['volume_up']:
                    if settings['volume'] + 1 <= 10: settings['volume'] += 1
                
                if event.key in settings['keybinds']['volume_up'] + settings['keybinds']['volume_down']:
                    self.volume_visible_time
                    self.volume_rect.y = 0

                    volume_noise = pygame.mixer.Sound('assets/sounds/volume.ogg')
                    volume_noise.set_volume(settings['volume'] / 10)
                    volume_noise.play()

                    #Write this change to 
                    write_settings(settings)

            self.state.handle_event(event)
    def set_state(self):
        next_state = self.state.next_state
        persistent_data = self.state.persistent_data

        #Set new state, pass persistent data
        if next_state in self.states.keys():
            self.state = self.states[next_state]
            self.state_name = list(self.states.keys())[list(self.states.values()).index(self.state)]
        else:
            print(f'Failed to find {next_state}. Reloading state')
        self.state.start(persistent_data)
    def tick(self, dt):
        if self.state.done: self.set_state()
        self.state.tick(dt) ######################

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
        for i in range(settings['volume']):
            rect = pygame.Rect(i * 12 + 20, 0, 8, (i + 1) * 2)
            rect.bottom = 30
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(rect.x + self.volume_rect.x, rect.y + self.volume_rect.y, rect.w, rect.h))
        self.screen.blit(self.volume_text, (self.volume_rect.x + 30, self.volume_rect.y + 34))

        if settings['preferences']['debug display']:
            self.screen.blit(self.fps_text, (6, 2))

    def run(self):
        while not self.done:

            dt = self.clock.tick(settings['preferences']['fps']) / 1000

            self.handle_events()
            if self.focused:
                self.tick(dt)
                self.draw()

            pygame.display.flip()