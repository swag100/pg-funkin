import pygame
import settings
import random
from .basestate import BaseState

from components.song import Song
from components.strumline import Strumline
from components.popup import Popup
from components.countdown import Countdown
from components.healthbar import HealthBar, BarIcon
from components.outlined_text import OutlinedText
from components.character import Character
from components.stage import Stage

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        self.just_created = False

    def start(self, persistent_data): 
        self.done = False
        self.persistent_data = persistent_data

        #THIS IS HARDCODED. FOR NOW, I'M WAY TOO LAZY AND DONT WANNA MAKE A WHOLE WEEKMENU STATE. SORRY!
        self.song_list = self.persistent_data['songs']
        #TODO: ^^^ Generate this list DYNAMICALLY with a given week file... And, also give the option TO PICK A DIFFICULTY.
        #These things require a main menu state, so if I'm really up for it, I'll make one... 

        self.week_progress = self.persistent_data['level progress'] #Current id for the song in the week you're in

        #contains chart reader object
        #will automatically start countdown
        self.song = Song(self.song_list[self.week_progress], 'hard')

        self.events = self.song.chart_reader.load_chart_events(self.song.song_name)

        print(self.song.song_name)

        if not self.just_created:
            self.just_created = True

            #CAMERA STUFF
            self.stage = Stage('mainStage')

            #cam zoom amounts
            self.cam_zoom = self.stage.cam_zoom
            self.hud_zoom = 1

            self.camera_position = [0, 0]
            self.camera_position_lerp = self.camera_position

        #game variables
        self.combo = 0
        self.health = settings.HEALTH_STARTING
        self.score = 0 #work on this tomorrow

        self.characters = [
            Character(self, self.song.characters['girlfriend'], self.stage.gf_position, 'girlfriend'),
            Character(self, self.song.characters['player'], self.stage.player_position, 'player'),
            Character(self, self.song.characters['opponent'], self.stage.opponent_position, 'opponent')
        ]

        #HUD STUFF

        #Health bar
        self.health_bar = HealthBar(self, (settings.SCREEN_CENTER[0], settings.WINDOW_SIZE[1] * 0.9))
        self.health_bar_icons = [
            BarIcon(self, self.song.characters['player'], True),
            BarIcon(self, self.song.characters['opponent'])
        ]

        #Score text
        self.score_text_font = pygame.font.Font('assets/fonts/vcr.ttf', 16)
        self.score_text_x = self.health_bar.lower_bar.x + self.health_bar.lower_bar.w - 190
        self.score_text_y = self.health_bar.lower_bar.y + 30

        #popup sprite group
        self.popups = []

        #Finally, create strums
        self.strums = []
        for i in range(8):
            self.strums.append(Strumline(i, self.song))

    def add_health(self, amount):
        if self.health + amount <= settings.HEALTH_MAX:
            self.health += amount
        else:
            self.health = settings.HEALTH_MAX

    def remove_health(self, amount):
        if self.health - amount >= settings.HEALTH_MIN:
            self.health -= amount
        else:
            self.health = settings.HEALTH_MIN
        
    def handle_event(self, event): 
        for strumline in self.strums: strumline.handle_event(event)
        for character in self.characters: character.handle_event(event)

        if event.type == pygame.USEREVENT:
            event_list = event.id.split('/', 1)
            event_type = event_list[0]
            try:
                event_parameters = event_list[1].split('/')
            except IndexError:
                event_parameters = []

            #if event_id in settings.HIT_WINDOWS.keys():
            if event_type == settings.NOTE_GOOD_HIT:
                rating = event_parameters[0]

                self.combo += 1 #Increase combo no matter the rating?

                self.add_health(settings.HEALTH_BONUSES[rating])

                #unmute player voice if it was
                if self.song.voices[0].get_volume() <= 0:
                    self.song.voices[0].set_volume(settings.volume)

                if rating in ['perfect', 'killer']: #Shares the same graphic
                    rating = 'sick'

                self.score += settings.SCORE_BONUSES[rating]

                #Create rating object, add rating to song.ratings list, award score
                self.popups.append(Popup(rating, settings.ratings_position))

                if self.combo >= 10:
                    combo_string = f'{self.combo:03}'
                    for i in range(len(combo_string)):
                        self.popups.append(Popup(f'num{combo_string[i]}', settings.combo_position, 0.5, i))

            #if event_id in settings.HEALTH_PENALTIES.keys():
            if event_type == settings.NOTE_MISS:
                self.combo = 0 # L
                
                #decrement health pretty
                self.score -= settings.SCORE_PENALTY
                self.remove_health(settings.HEALTH_PENALTIES[event_parameters[0]])

                miss_noise = pygame.mixer.Sound(f'assets/sounds/gameplay/missnote{random.randint(1, 3)}.ogg')
                miss_noise.set_volume(settings.volume * 0.4)
                miss_noise.play()

                #voices[0] is players voice
                #mute player vocals until palyer gets a rating
                self.song.voices[0].set_volume(0)
            
            if event_type == settings.BEAT_HIT: #BEAT HIT
                cur_beat = int(event_parameters[0]) #easier to read

                if cur_beat == 0:
                    self.song.play_audio()

                #Countdown : )
                if -4 <= cur_beat < 0:
                    countdown_noises = [
                        pygame.mixer.Sound(f'assets/sounds/countdown/introTHREE.ogg'),
                        pygame.mixer.Sound(f'assets/sounds/countdown/introTWO.ogg'),
                        pygame.mixer.Sound(f'assets/sounds/countdown/introONE.ogg'),
                        pygame.mixer.Sound(f'assets/sounds/countdown/introGO.ogg'),
                    ]
                    countdown_images = [
                        'ready',
                        'set',
                        'go'
                    ]
                    countdown_noises[cur_beat + 4].set_volume(settings.volume)
                    countdown_noises[cur_beat + 4].play()

                    #image
                    if -3 <= cur_beat < 0:
                        self.popups.append(Countdown(countdown_images[cur_beat + 3], settings.SCREEN_CENTER))

                #Cam zoom on beat hit
                if cur_beat % 4 == 0:
                    self.hud_zoom = 1.02

                for icon in self.health_bar_icons:
                    icon.bump()

                """
                high_beep = pygame.mixer.Sound("assets/sounds/metronome1.ogg")
                high_beep.set_volume(settings.volume)
                low_beep = pygame.mixer.Sound("assets/sounds/metronome2.ogg")
                low_beep.set_volume(settings.volume)
                if self.song.conductor.cur_beat >= 0: 
                    if self.song.conductor.cur_beat % 4 == 0:
                        high_beep.play()
                    else:
                        low_beep.play()
                """

            """
            if event_type == settings.SONG_BEGAN:
                print('Hello, song! You just started :)')
            """
                
            if event_type == settings.SONG_ENDED:
                #print('Song over!')

                self.persistent_data['level progress'] += 1
                if self.persistent_data['level progress'] > len(self.song_list):
                    print('Level finished.')
                    return

                self.next_state = 'PlayState'
                self.done = True

                
            
    def handle_chart_events(self, chart_event):
        event_var = chart_event['variable']

        if chart_event['time'] / 1000 <= self.song.conductor.song_position: #SHOULD BE ACTIVATED
            #FOCUS CAMERA
            if chart_event['type'] == 'FocusCamera':
                if isinstance(event_var, dict):
                    event_var = event_var['char']

                if bool(event_var):
                    self.camera_position = [
                        self.stage.opponent_position[0] + self.stage.opponent_cam_off[0],
                        self.stage.opponent_position[1] + self.stage.opponent_cam_off[1]
                    ]
                else:
                    self.camera_position = [
                        self.stage.player_position[0] + self.stage.player_cam_off[0],
                        self.stage.player_position[1] + self.stage.player_cam_off[1]
                    ]
            #PLAY ANIMATION
            if chart_event['type'] == 'PlayAnimation':
                target = event_var['target']
                anim_to_play = event_var['anim']

                for character in self.characters:
                    if target == character.character:
                        character.play_animation(anim_to_play)

            #FINALLY, REMOVE EVENT
            self.events.remove(chart_event)


    def tick(self, dt):
        if dt > 1: return

        #This also ticks conductor
        self.song.tick(dt)

        #update cam lerp
        self.camera_position_lerp[0] += (self.camera_position[0] - self.camera_position_lerp[0]) * (dt * settings.CAMERA_SPEED)
        self.camera_position_lerp[1] += (self.camera_position[1] - self.camera_position_lerp[1]) * (dt * settings.CAMERA_SPEED)

        #CHARTING EVENTS
        for event in self.events: self.handle_chart_events(event)

        #game objects

        self.stage.tick(dt, self.camera_position_lerp)
        for character in self.characters: character.tick(dt, self.camera_position_lerp)

        #hud
        self.health_bar.tick(dt)

        self.score_text_string = f'Score: {int(self.score):,}'

        for icon in self.health_bar_icons: icon.tick(dt)

        for strumline in self.strums: 
            strumline.tick(dt)

            if not strumline.bot_strum:
                for sustain in strumline.sustains:
                    if sustain.being_eaten:
                        self.score += settings.SCORE_BONUSES['holding'] * dt
                        self.add_health(settings.HEALTH_BONUSES['holding'] * dt)
            
        for popup in self.popups: 
            popup.tick(dt)

            if popup.alpha <= 0:
                self.popups.remove(popup)

        #Reset surfaces every tick.
        self.cam_surface = pygame.Surface(settings.WINDOW_SIZE, pygame.SRCALPHA)
        self.hud_surface = pygame.Surface(settings.WINDOW_SIZE, pygame.SRCALPHA)

        self.hud_zoom += (1 - self.hud_zoom) / 8

        
        #TESTING CAMERA CODE:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]: self.camera_position[0] -= 500 * dt
        if keys[pygame.K_l]: self.camera_position[0] += 500 * dt
        if keys[pygame.K_i]: self.camera_position[1] -= 500 * dt
        if keys[pygame.K_k]: self.camera_position[1] += 500 * dt
        

        #for note in self.song.chart_reader.chart: note.tick(dt)

    def draw(self, screen):
        #screen.fill((255, 255, 255))

        #game
        self.stage.draw(self.cam_surface)
        for character in self.characters: character.draw(self.cam_surface)

        #hud
        for strumline in self.strums: strumline.draw(self.hud_surface)
        for popup in self.popups: popup.draw(self.hud_surface)

        #Draw the healthbar.
        self.health_bar.draw(self.hud_surface)
        for icon in self.health_bar_icons: icon.draw(self.hud_surface)

        #Draw the outline for the scoretext, then draw the scoretext itself.
        self.score_text = OutlinedText(self.score_text_string, (self.score_text_x, self.score_text_y), 1, 16, self.hud_surface, self.score_text_font)
        self.score_text.draw()
        #self.hud_surface.blit(text, self.score_text_rect)

        #cameras - This code is really ugly, i know.
        scaled_cam_surface = pygame.transform.smoothscale_by(self.cam_surface, self.cam_zoom)
        scaled_hud_surface = pygame.transform.smoothscale_by(self.hud_surface, self.hud_zoom)
        screen.blit(scaled_cam_surface, self.cam_surface.get_rect(center = settings.SCREEN_CENTER))
        screen.blit(scaled_hud_surface, scaled_hud_surface.get_rect(center = settings.SCREEN_CENTER))
        
        #for note in self.song.chart_reader.chart: note.draw(screen)