import pygame as pg
from game.scripts.text.text import Text
from game.scripts.images.image import Image
from game.scripts.images.button import Button

from game.scripts.utilities.json.load_json_dialog import LoadJsonDialog


class Dialog:
    def __init__(self, dialog, screen):
        self.texts = LoadJsonDialog(dialog)
        self.idx = "start"
        self.now = self.texts.get_text(self.idx)
        self.text = Text(self.now, 20, (40, 350), (100, 100, 100), screen)
        self.set_dialog()
        self.image = Image("dialog/dialog", (0, 313), screen)
        self.next_button = Button((1000, 500), screen, "Next")
        self.next_button.set_scale(0.5)

        self.is_visible = True

    def blit(self):
        if self.is_visible:
            self.check()
            self.image.blit()
            self.text.blit()
            self.next_button.blit()

    def check(self):
        if self.next_button.is_mouse_click_button():
            self.set_dialog()

    def set_dialog(self):

        if self.idx != "end":
            self.text.set_text(self.now)
        else:
            self.is_visible = False

        self.idx = self.texts.get_next(self.idx)
        self.now = self.texts.get_text(self.idx)
