import pygame
import constants
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
from components.alphabet import Alphabet

class PlayState(BaseState):
    def start(self, persistent_data): 
        super(PlayState, self).__init__()
        self.persistent_data = persistent_data

        self.song_list = persistent_data['songs']
        self.difficulty = persistent_data['difficulty']

        self.previous_state = None
        if 'previous state' in persistent_data:
            self.previous_state = persistent_data['previous state']

        self.level_progress = 0
        if 'level progress' in persistent_data:
            self.level_progress = persistent_data['level progress'] #Current id for the song in the week you're in

        #contains chart reader object
        #will automatically start countdown
        self.song = Song(self.song_list[self.level_progress], self.difficulty)
        self.events = self.song.chart_reader.load_chart_events(self.song.song_name)

        self.player_voice_track_muted = False

        #PAUSE stuff C:
        self.paused = False
        self.pause_option_objects = []
        self.pause_options = [
            'resume',
            'restart song',
            'exit to menu'
        ]
        for i in range(len(self.pause_options)):
            self.pause_option_objects.append(Alphabet(self.pause_options[i]))
        self.pause_selection = 0

        #TODO: Only create stage if A: There was NO previous stage or B: If the previous stage is != to self.song.stage

        #STAGE STUFF!
        self.stage = Stage(self.song.stage)

        #TODO: Only create characters if A: There was NO previous characters or B: If the previous character is != to self.song.characters['whichever one']

        #create characters
        self.characters = {
            'girlfriend': Character(self, self.song.characters['girlfriend'], self.stage.gf_position, 'girlfriend'),
            'player': Character(self, self.song.characters['player'], self.stage.player_position, 'player'),
            'opponent': Character(self, self.song.characters['opponent'], self.stage.opponent_position, 'opponent')
        }

        #cam zoom amount: taken from stage data!
        self.cam_zoom = self.stage.cam_zoom
        self.hud_zoom = 1
        
        #Make player start with their idle, so you don't see a death sprite when restarting a song.
        self.characters['player'].play_animation('idle')

        #game variables
        self.combo = 0
        self.score = 0

        self.health = constants.HEALTH_STARTING
        self.health_lerp = self.health #The pretty health value we draw the healthbar with.

        #Do not tween cam or healthbar if we weren't previously in PlayState!!
        if self.previous_state != 'PlayState':
            self.camera_position = [0, 0]
            self.camera_position_lerp = self.camera_position
        else:
            if 'old health' in self.persistent_data:
                #For a squeaky clean transition between songs! :D
                self.health_lerp = self.persistent_data['old health']

        #HUD STUFF

        #Health bar
        self.health_bar = HealthBar(self, (constants.SCREEN_CENTER[0], constants.WINDOW_SIZE[1] * 0.9))
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
    
    def die(self):
        self.song.stop_audio()

        self.persistent_data['cam position'] = self.camera_position_lerp
        self.persistent_data['cam zoom'] = self.cam_zoom
        self.persistent_data['player'] = self.characters['player'] #much easier to just pass the bf object.

        self.next_state = 'GameOverState'
        self.done = True

    def add_health(self, amount):
        if self.health + amount <= constants.HEALTH_MAX:
            self.health += amount
        else:
            self.health = constants.HEALTH_MAX

    def remove_health(self, amount):
        if self.health - amount >= constants.HEALTH_MIN:
            self.health -= amount
        else:
            self.die()
            #self.health = constants.HEALTH_MIN
    
    def toggle_pause(self):
        self.paused = not self.paused
        self.song.toggle_pause()
    
    def increment_pause_selection(self, increment):
        self.pause_selection += increment
        #lower limit
        if self.pause_selection < 0:
            self.pause_selection = len(self.pause_options) - 1
        #upper limit
        if self.pause_selection > len(self.pause_options) - 1:
            self.pause_selection = 0
        
    def handle_event(self, event): 
        if event.type == pygame.KEYDOWN:
            if self.paused:
                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_up']:
                    self.scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                    self.scroll_sound.play()
                    
                    self.increment_pause_selection(-1)

                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['menu_down']:
                    self.scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                    self.scroll_sound.play()

                    self.increment_pause_selection(1)

                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                    #SORRY for hardcoding this. Please. Forgive me.
                    selection = self.pause_options[self.pause_selection]
                    if selection == 'resume' or selection not in self.pause_options:
                        self.toggle_pause()
                    if selection == 'restart song':
                        self.persistent_data['old health'] = self.health_lerp
                        self.persistent_data['previous state'] = 'PlayState'
                        self.next_state = 'PlayState'
                        self.done = True
                    if selection == 'exit to menu':
                        self.next_state = 'MainMenuState'
                        self.done = True
            else:
                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward'] or event.key in constants.SETTINGS_DEFAULT_KEYBINDS['back']:
                    self.toggle_pause()

                    self.scroll_sound = pygame.mixer.Sound('assets/sounds/scrollMenu.ogg')
                    self.scroll_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                    self.scroll_sound.play()

                    for alphabet in self.pause_option_objects: 
                        alphabet.x = 0
                        alphabet.y = 0
                if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['reset']:
                    self.die()

        if self.paused: return

        for strumline in self.strums: strumline.handle_event(event)
        for character in self.characters.values(): character.handle_event(event)

        if event.type == pygame.USEREVENT:
            event_list = event.id.split('/', 1)
            event_type = event_list[0]
            try:
                event_parameters = event_list[1].split('/')
            except IndexError:
                event_parameters = []

            #if event_id in settings.HIT_WINDOWS.keys():
            if event_type == constants.NOTE_GOOD_HIT:
                rating = event_parameters[0]

                self.combo += 1 #Increase combo no matter the rating?

                self.add_health(constants.HEALTH_BONUSES[rating])

                #unmute player voice if it was
                self.player_voice_track_muted = False

                if rating in ['perfect', 'killer']: #Shares the same graphic
                    rating = 'sick'

                self.score += constants.SCORE_BONUSES[rating]

                #Create rating object, add rating to song.ratings list, award score
                self.popups.append(Popup(rating, constants.SETTINGS_DEFAULT_RATING_POSITION))

                if self.combo >= 10:
                    combo_string = f'{self.combo:03}'
                    for i in range(len(combo_string)):
                        self.popups.append(Popup(f'num{combo_string[i]}', constants.SETTINGS_DEFAULT_COMBO_POSITION, 0.5, i))

            #if event_id in settings.HEALTH_PENALTIES.keys():
            if event_type == constants.NOTE_MISS:
                self.combo = 0 # L
                
                #decrement health pretty
                self.score -= constants.SCORE_PENALTY
                self.remove_health(constants.HEALTH_PENALTIES[event_parameters[0]])

                miss_noise = pygame.mixer.Sound(f'assets/sounds/gameplay/missnote{random.randint(1, 3)}.ogg')
                miss_noise.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 20) #20 is intentional; should be way quieter.
                pygame.mixer.Channel(2).play(miss_noise)
                #miss_noise.play()

                #voices[0] is players voice
                #mute player vocals until palyer gets a rating
                self.player_voice_track_muted = True
            
            if event_type == constants.BEAT_HIT: #BEAT HIT
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
                    countdown_noises[cur_beat + 4].set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                    countdown_noises[cur_beat + 4].play()

                    #image
                    if -3 <= cur_beat < 0:
                        self.popups.append(Countdown(countdown_images[cur_beat + 3], constants.SCREEN_CENTER))

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
                
            if event_type == constants.SONG_ENDED:
                self.persistent_data['level progress'] = self.level_progress + 1
                
                self.persistent_data['old health'] = self.health_lerp
                self.persistent_data['previous state'] = 'PlayState'
                self.next_state = 'PlayState'

                if self.persistent_data['level progress'] >= len(self.song_list):
                    self.next_state = 'MainMenuState'

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

                for character in self.characters.values():
                    if target == character.character:
                        character.play_animation(anim_to_play)

            #FINALLY, REMOVE EVENT
            self.events.remove(chart_event)

    def tick(self, dt):
        if self.paused:
            for alphabet in self.pause_option_objects: 
                i = self.pause_option_objects.index(alphabet) - self.pause_selection

                #lerp them to the selection position
                selection_position = (100, constants.SCREEN_CENTER[1])
                #alphabet.x = i * 50
                #alphabet.y = i * 80
                alphabet.x += ((selection_position[0] + (i * 25)) - alphabet.x) * (dt * 6)
                alphabet.y += ((selection_position[1] + (i * 150)) - alphabet.y) * (dt * 6)

                alphabet.tick(dt)
            return

        if dt > self.song.conductor.crochet: return

        #This also ticks conductor
        self.song.tick(dt, self.player_voice_track_muted)

        #update cam lerp
        self.camera_position_lerp[0] += (self.camera_position[0] - self.camera_position_lerp[0]) * (dt * constants.SETTINGS_DEFAULT_CAMERA_SPEED)
        self.camera_position_lerp[1] += (self.camera_position[1] - self.camera_position_lerp[1]) * (dt * constants.SETTINGS_DEFAULT_CAMERA_SPEED)

        #update health lerp
        self.health_lerp += (self.health - self.health_lerp) * (dt * 10)

        #CHART EVENTS
        for event in self.events: self.handle_chart_events(event)

        #game objects

        self.stage.tick(dt, self.camera_position_lerp)
        for character in self.characters.values(): character.tick(dt, self.camera_position_lerp)

        #hud
        self.health_bar.tick(dt)

        self.score_text_string = f'Score: {int(self.score):,}'

        for icon in self.health_bar_icons: icon.tick(dt)

        for strumline in self.strums: 
            strumline.tick(dt)

            if not strumline.bot_strum:
                for sustain in strumline.sustains:
                    if sustain.being_eaten:
                        self.score += constants.SCORE_BONUSES['holding'] * dt
                        self.add_health(constants.HEALTH_BONUSES['holding'] * dt)
            
        for popup in self.popups: 
            popup.tick(dt)

            if popup.alpha <= 0:
                self.popups.remove(popup)

        self.hud_zoom += (1 - self.hud_zoom) / 8

        """
        #TESTING CAMERA CODE:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]: self.camera_position[0] -= 500 * dt
        if keys[pygame.K_l]: self.camera_position[0] += 500 * dt
        if keys[pygame.K_i]: self.camera_position[1] -= 500 * dt
        if keys[pygame.K_k]: self.camera_position[1] += 500 * dt
        """

        #for note in self.song.chart_reader.chart: note.tick(dt)

    def draw(self, screen):
        #screen.fill((255, 255, 255))

        #Start out by resetting the surfaces completely.
        cam_surface = pygame.Surface(constants.WINDOW_SIZE)
        hud_surface = pygame.Surface(constants.WINDOW_SIZE, pygame.SRCALPHA)

        #game
        self.stage.draw(cam_surface)
        for character in self.characters.values(): character.draw(cam_surface)

        #hud
        for strumline in self.strums: strumline.draw(hud_surface)
        for popup in self.popups: popup.draw(hud_surface)

        #Draw the healthbar.
        self.health_bar.draw(hud_surface)
        for icon in self.health_bar_icons: icon.draw(hud_surface)

        #Draw the outline for the scoretext, then draw the scoretext itself.
        score_text = OutlinedText(self.score_text_string, (self.score_text_x, self.score_text_y), 1, 16, hud_surface, self.score_text_font)
        score_text.draw()
        #hud_surface.blit(text, self.score_text_rect)

        #cameras - This code is really ugly, i know.
        scaled_cam_surface = pygame.transform.smoothscale_by(cam_surface, self.cam_zoom)
        scaled_hud_surface = pygame.transform.smoothscale_by(hud_surface, self.hud_zoom)
        screen.blit(scaled_cam_surface, cam_surface.get_rect(center = constants.SCREEN_CENTER))
        screen.blit(scaled_hud_surface, scaled_hud_surface.get_rect(center = constants.SCREEN_CENTER))

        if self.paused:
            cover = pygame.Surface(constants.WINDOW_SIZE, pygame.SRCALPHA)
            cover.fill((0,0,0,255 * 0.6))
            screen.blit(cover, (0,0))

            for alphabet in self.pause_option_objects: 
                #Make the selection the only one with full transparency.
                for character in alphabet.character_list:
                    character.animation.getCurrentFrame().set_alpha(128)

                    if self.pause_selection == self.pause_option_objects.index(alphabet):
                        character.animation.getCurrentFrame().set_alpha(255)

                alphabet.draw(screen)

        #for note in self.song.chart_reader.chart: note.draw(screen)