import pygame as pg


class Text:
    def __init__(self, text, size, position, color, screen):
        self.color = color
        self.font = pg.font.SysFont("Arial", size)
        self.text = self.font.render(text, True, color)
        self.text_position = position
        self.screen = screen

    def blit(self):
        self.screen.blit(self.text, self.text_position)

    def set_text(self, text):
        self.text = self.font.render(text, True, self.color)

    def set_scale(self, scale):
        self.text = pg.transform.scale(self.text, (self.text.get_width() * scale, self.text.get_height() * scale))

    def move_position(self, position):
        self.text_position = (self.text_position[0] + position[0], self.text_position[1] + position[1])
