import pygame
import constants
from states.basestate import BaseState

class GameOverState(BaseState):
    def start(self, persistent_data):
        super(GameOverState, self).__init__()

        self.persistent_data = persistent_data

        self.camera_position_lerp = (0, 0)
        if 'cam position' in persistent_data:
            self.camera_position_lerp = persistent_data['cam position']

        self.cam_zoom = 1
        if 'cam zoom' in persistent_data:
            self.cam_zoom = persistent_data['cam zoom']
        
        self.player = None
        if 'player' in persistent_data:
            self.player = persistent_data['player']

        self.camera_position = (0, 0)
        if self.player != None:
            self.camera_position = (
                self.player.screen_pos[0] - 500, 
                self.player.screen_pos[1] - 250
            )

            self.player.play_animation('firstDeath')

        self.is_retrying = False
        self.retry_time = 5 #How many seconds does it take to play the retry animation?
        self.retry_time_elapsed = 0

        self.player_alpha = 255 * 1.7

        death_sound = pygame.Sound('assets/sounds/gameplay/fnf_loss_sfx.ogg')
        death_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
        death_sound.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['back']:
                pass #go to main menu

            if event.key in constants.SETTINGS_DEFAULT_KEYBINDS['forward']:
                if self.is_retrying: return

                if self.player != None: self.player.play_animation('deathConfirm')
                self.is_retrying = True

                pygame.mixer.music.stop()
                retry_sound = pygame.Sound('assets/music/gameOverEnd.ogg')
                retry_sound.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)
                retry_sound.play()

    def tick(self, dt):
        if self.is_retrying: self.retry_time_elapsed += dt

        if self.retry_time_elapsed >= self.retry_time:
            self.persistent_data['previous state'] = 'GameOverState'
            self.next_state = 'PlayState'
            self.done = True

        #update cam lerp: I purposefully made this slower.
        self.camera_position_lerp[0] += (self.camera_position[0] - self.camera_position_lerp[0]) * (dt * constants.SETTINGS_DEFAULT_CAMERA_SPEED / 2)
        self.camera_position_lerp[1] += (self.camera_position[1] - self.camera_position_lerp[1]) * (dt * constants.SETTINGS_DEFAULT_CAMERA_SPEED / 2)

        if self.player != None:
            self.player.tick(dt, self.camera_position_lerp)
            
            if self.is_retrying:
                self.player_alpha -= 128 * dt

            if self.player.animation.isFinished() and self.player.anim_prefix == 'firstDeath':
                self.player.play_animation('deathLoop', True)
                pygame.mixer.music.load('assets/music/gameOver.ogg')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(constants.SETTINGS_DEFAULT_VOLUME / 10)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        pygame.transform.smoothscale_by(screen, self.cam_zoom)

        if self.player != None:
            self.player.animation.getCurrentFrame().set_alpha(self.player_alpha)
            self.player.draw(screen)