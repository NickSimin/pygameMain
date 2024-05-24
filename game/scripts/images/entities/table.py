import pygame as pg
from game.scripts.images.entities.entities import Entity
from game.scripts.text.dialog.dialog import Dialog


class Table(Entity):
    def __init__(self, position, screen, dialog):
        super().__init__("tiles/spawners/2", position, screen)

        self.player_type = False
        self.dialog = dialog

    def check(self, player):
        if self.is_collide(player):
            self.dialog.is_visible = True

    def blit(self, cord=None):
        self.dialog.blit()
        if cord is None:
            self.screen.blit(self.image, self.position)
        else:
            self.screen.blit(self.image, (self.position[0] + cord[0], self.position[1] + cord[1]))
