import pygame as pg
from game.scripts.images.image import Image
from game.scripts.text.text import Text


class Button(Image):
    def __init__(self, position, screen, text):
        super().__init__("button", position, screen)
        self.text = Text(text, 50, (self.position[0] - self.image.get_width() / 4 + 20,
                                    self.position[1] - self.image.get_height() / 3), screen)

        self.position = (position[0] - self.image.get_width() / 2, position[1] - self.image.get_height() / 2)

    def blit(self):
        self.screen.blit(self.image, self.position)
        self.text.blit()


