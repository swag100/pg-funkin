import pygame

from components.spritesheet import Spritesheet

Y_OFFSETS = {
    'regular': {
        '-': -15
    }
}

class Letter:
    def __init__(self, alphabet, i, x_off):
        self.alphabet = alphabet
        self.sheet = self.alphabet.sheet
        self.text = self.alphabet.text
        self.index = i
        self.x_off = x_off

        self.character = self.text[self.index]

        if self.alphabet.font == 'bold':
            self.character = self.character.upper()

        self.animation = self.sheet.frames_to_animation(self.sheet.load_anim_frames(f'{self.character} {self.alphabet.font}'))
        self.animation.play(True)

        self.anim_size = self.animation.getMaxSize()
        self.rect = pygame.Rect(0, 0, self.anim_size[0], self.anim_size[1])

    def tick(self, dt):
        self.rect.x = self.alphabet.x
        self.rect.y = self.alphabet.y

        self.rect.x += self.x_off
        
        self.rect.bottom = self.alphabet.y # + (50 * self.alphabet.scale)

        if self.alphabet.font in Y_OFFSETS and self.character in Y_OFFSETS[self.alphabet.font]:
            self.rect.y += Y_OFFSETS[self.alphabet.font][self.character] * self.alphabet.scale

        self.animation.tickFrameNum()

    def draw(self, screen):
        self.animation.blit(screen, self.rect)

class Alphabet:
    def __init__(self, text, pos = [0, 0], scale = 1, spacing = 0, font = 'bold'):
        self.sheet = Spritesheet(f'assets/images/fonts/{font}.png', scale)
        self.font = font
        self.scale = scale

        self.text = text
        self.character_list = []

        self.x = pos[0]
        self.y = pos[1]

        self.width = 0
        for i in range(len(self.text)):
            if self.text[i] != ' ':
                try:
                    letter = Letter(self, i, self.width)
                    self.width += (letter.rect.w + spacing) #add width of letter and 4 extra pixels for spacing.
                    self.character_list.append(letter)
                except:
                    self.width += 40 * scale

            else:
                self.width += 40 * scale
        
    def tick(self, dt):
        for character in self.character_list: character.tick(dt)

    def draw(self, screen):
        for character in self.character_list: character.draw(screen)