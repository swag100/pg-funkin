import pygame


class OutlinedText(object):
    def __init__(
            self,
            text,
            position,
            outline_width,
            font_size,
            screen,
            font,
            foreground_color=(255, 255, 255),
            background_color=(0, 0, 0)
    ):
        """
        Outline text for pygame.
        :param text: bytes or unicode text
        :param position: tuple of form (x, y) you wish text to be rendered at
        :param outline_width: outline width in pixels
        :param font_size: font size
        :param screen: pygame screen you want text rendered to
        :param foreground_color: foreground color of text defaults to white
        :param background_color: background color of text defaults to black
        """
        self.text = text
        self.position = position
        self.foreground = foreground_color
        self.background = background_color
        self.outline_width = outline_width
        self.screen = screen
        self.font = font
        self.text_surface = self.font.render(self.text, True, self.foreground)
        self.text_outline_surface = self.font.render(self.text, True, self.background)
        self.alpha = 1
        # There is no good way to get an outline with pygame, so we draw
        # the text at 8 points around the main text to simulate an outline.
        self.directions = [
            (self.outline_width, self.outline_width),
            (0, self.outline_width),
            (-self.outline_width, self.outline_width),
            (self.outline_width, 0),
            (-self.outline_width, 0),
            (self.outline_width, -self.outline_width),
            (0, -self.outline_width),
            (-self.outline_width, -self.outline_width)
        ]

    def get_width(self):
        """
        Get width of text including border.
        :return: width of text, including border.
        """
        return self.text_surface.get_width() + self.outline_width * 2

    def change_position(self, position):
        """
        change position text is blitted to.
        :param position: tuple in the form of (x, y)
        :return:
        """
        self.position = position

    def change_text(self, text):
        """
        Changes text to "text"
        :param text: New text
        """
        self.text = text
        self._update_text()

    def change_foreground_color(self, color):
        """
        Changes foreground color
        :param color: New foreground color
        """
        self.foreground = color
        self._update_text()

    def change_outline_color(self, color):
        """
        Changes the outline color
        :param color: New outline color
        """
        self.background = color
        self._update_text()

    def _update_text(self):
        """
        "protected" function to replace the text surface with a new one based on updated values.
        """
        self.text_surface = self.font.render(self.text, True, self.foreground)
        self.text_outline_surface = self.font.render(self.text, True, self.background)

    def draw(self):
        # blit outline images to screen
        for direction in self.directions:
            self.text_outline_surface.set_alpha(self.alpha * 255)
            self.screen.blit(
                self.text_outline_surface,
                (
                    self.position[0] - direction[0],
                    self.position[1] - direction[1]
                )
            )
        # blit foreground image to the screen
        self.text_surface.set_alpha(self.alpha * 255)
        self.screen.blit(self.text_surface, self.position)
