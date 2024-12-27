import pygame
import constants

from components.spritesheet import Spritesheet

letter_offsets = {
    'A': (0, 0),
    'B': (0, 0),
    'C': (0, 0),
    'D': (0, 0),
    'E': (0, 0),
    'F': (0, 0),
    'G': (0, 0),
    'H': (0, 0),
    'I': (0, 0),
    'J': (0, 0),
    'K': (0, 0),
    'L': (0, 0),
    'M': (0, 0),
    'N': (0, 0),
    'O': (0, 0),
    'P': (0, 0),
    'Q': (0, 0),
    'R': (0, 0),
    'S': (0, 0),
    'T': (0, 0),
    'U': (0, 0),
    'V': (0, 0),
    'W': (0, 0),
    'X': (0, 0),
    'Y': (0, 0),
    'Z': (0, 0)
}

class Letter:
    def __init__(self, alphabet, i, x_off):
        self.alphabet = alphabet
        self.sheet = self.alphabet.sheet
        self.text = self.alphabet.text
        self.index = i
        self.x_off = x_off

        self.character = self.text[self.index].upper()

        self.animation = self.sheet.frames_to_animation(self.sheet.load_animation(f'{self.character} bold'))
        self.animation.play(True)

        anim_size = self.animation.getMaxSize()
        self.rect = pygame.Rect(0, 0, anim_size[0], anim_size[1])

    def tick(self, dt):

        self.rect.x = self.alphabet.x
        self.rect.y = self.alphabet.y

        self.rect.x += self.x_off

        self.animation.tickFrameNum()

    def draw(self, screen):
        self.animation.blit(screen, self.rect)

class Alphabet:
    def __init__(self, text, pos = [0, 0], scale = 1):
        self.sheet = Spritesheet('assets/images/alphabet.png', scale)
        self.scale = scale

        self.text = text
        self.character_list = []

        self.x = pos[0]
        self.y = pos[1]

        character_x = 0
        for i in range(len(self.text)):
            if self.text[i] != ' ':
                letter = Letter(self, i, character_x)
                character_x += (letter.rect.w + 1) * scale #add width of letter and 4 extra pixels for spacing.
                self.character_list.append(letter)
            else:
                character_x += 40 * scale
        
    def tick(self, dt):
        for character in self.character_list: character.tick(dt)

    def draw(self, screen):
        for character in self.character_list: character.draw(screen)