import pygame as pg


class Text:
    def __init__(self, text, size, position, screen):
        self.font = pg.font.SysFont("Arial", size)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.position = position
        self.screen = screen

    def blit(self):
        self.screen.blit(self.text, self.position)