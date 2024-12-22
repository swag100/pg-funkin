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

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()

        #contains chart reader object
        #will automatically start countdown
        self.song = Song('fresh', 'hard')

        #game variables
        self.combo = 0
        self.health = settings.HEALTH_STARTING
        self.score = 0 #work on this tomorrow

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

        #create strums
        self.strums = []
        for i in range(8):
            self.strums.append(Strumline(i, self.song))

        #cam zoom amounts
        self.cam_zoom = 1
        self.hud_zoom = 1

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

        if event.type == pygame.USEREVENT:
            if event.id in settings.HIT_WINDOWS.keys():
                self.combo += 1 #Increase combo no matter the rating?

                self.add_health(settings.HEALTH_BONUSES[event.id])

                #unmute player voice if it was
                if self.song.voices[0].get_volume() <= 0:
                    self.song.voices[0].set_volume(settings.volume)

                rating = event.id
                if event.id in ['perfect', 'killer']: #Shares the same graphic
                    rating = 'sick'

                self.score += settings.SCORE_BONUSES[rating]

                #Create rating object, add rating to song.ratings list, award score
                self.popups.append(Popup(rating, settings.ratings_position))

                if self.combo >= 10:
                    combo_string = f'{self.combo:03}'
                    for i in range(len(combo_string)):
                        self.popups.append(Popup(f'num{combo_string[i]}', settings.combo_position, 0.5, i))

            if event.id in settings.HEALTH_PENALTIES.keys():
                self.combo = 0 # L
                
                #decrement health pretty
                self.score -= settings.SCORE_PENALTY
                self.remove_health(settings.HEALTH_PENALTIES[event.id])

                miss_noise = pygame.mixer.Sound(f'assets/sounds/gameplay/missnote{random.randint(1, 3)}.ogg')
                miss_noise.set_volume(settings.volume * 0.4)
                miss_noise.play()

                #voices[0] is players voice
                #mute player vocals until palyer gets a rating
                self.song.voices[0].set_volume(0)

            
            if event.id == settings.BEAT_HIT: #BEAT HIT
                beat = self.song.conductor.cur_beat #easier to read

                if beat == 0:
                    self.song.play_audio()

                #Countdown : )
                if -4 <= beat < 0:
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
                    countdown_noises[beat + 4].set_volume(settings.volume)
                    countdown_noises[beat + 4].play()

                    #image
                    if -3 <= beat < 0:
                        self.popups.append(Countdown(countdown_images[beat + 3], settings.SCREEN_CENTER))

                #Cam zoom on beat hit
                if beat % 4 == 0:
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
            

    def tick(self, dt):
        self.song.conductor.tick(dt)
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

        #for note in self.song.chart_reader.chart: note.tick(dt)

    def draw(self, screen):
        screen.fill((255, 255, 255))

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
        cam_rect = scaled_cam_surface.get_rect(center = settings.SCREEN_CENTER)
        hud_rect = scaled_hud_surface.get_rect(center = settings.SCREEN_CENTER)
        screen.blit(scaled_cam_surface, cam_rect)
        screen.blit(scaled_hud_surface, hud_rect)
        
        #for note in self.song.chart_reader.chart: note.draw(screen)