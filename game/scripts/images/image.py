import pygame as pg
from game.scripts.utilities.load.load_image import load_image


class Image:
    def __init__(self, path, position, screen):
        self.image = load_image(path)
        self.position = position
        self.screen = screen
        self.size = self.image.get_size()

    def blit(self):
        self.screen.blit(self.image, self.position)

    def is_mouse_hover(self):
        if self.position[0] < pg.mouse.get_pos()[0] < self.position[0] + self.image.get_width():
            if self.position[1] < pg.mouse.get_pos()[1] < self.position[1] + self.image.get_height():
                return True
        return False

    def is_mouse_click(self):
        if self.is_mouse_hover():
            if pg.mouse.get_pressed()[0]:
                return True
        return False

    def is_collide(self, other):
        if self.is_collide_height(other) and self.is_collide_width(other):
            return True
        return False

    def is_collide_height(self, other):
        x1 = self.position[0]
        x2 = other.position[0]
        width1 = self.size[0]
        width2 = other.size[0]

        if x2 - width1 <= x1 <= x2 + width2:
            return True
        return False

    def is_collide_width(self, other):
        y1 = self.position[1]
        y2 = other.position[1]
        height1 = self.size[1]
        height2 = other.size[1]

        if y2 - height1 <= y1 <= y2 + height2:
                return True
        return False


class Background(Image):
    def __init__(self, path, screen, size):
        super().__init__(path, (0, 0), screen)
        self.image = pg.transform.scale(self.image, (size[0], size[1]))
