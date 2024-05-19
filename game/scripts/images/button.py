import pygame as pg
from game.scripts.images.image import Image
from game.scripts.text.text import Text


class Button(Image):
    def __init__(self, position, screen, text):
        super().__init__("button", position, screen)
        self.text = Text(text, 50, (self.position[0] - self.image.get_width() / 4 + 20,
                                    self.position[1] - self.image.get_height() / 3), (255, 255, 255), screen)
        self.position = (position[0] - self.image.get_width() / 2, position[1] - self.image.get_height() / 2)
        self.click_check = True

    def blit(self):
        self.check_click()
        self.screen.blit(self.image, self.position)
        self.text.blit()

    def set_scale(self, scale):
        self.image = pg.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.text.set_scale(scale)
        self.text.move_position((-self.image.get_width() / 4 - 10, -self.image.get_height() / 4 + 5))

    def is_mouse_click_button(self):
        if self.is_mouse_click() and self.click_check:
            self.click_check = False
            return True
        return False

    def check_click(self):
        if not self.is_mouse_click():
            self.click_check = True
