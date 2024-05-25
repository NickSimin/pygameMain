import pygame as pg
from game.scripts.images.entities.entities import Entity


class Exit(Entity):
    def __init__(self, position, screen, next_level, tilemap, player):
        super().__init__("tiles/spawners/1", position, screen)
        self.next_level = str(next_level)
        self.tilemap = tilemap
        self.player_type = True
        self.player = player

    def check(self, player):
        if self.is_collide(player):
            self.next()

    def next(self):
        print("check2")
        if self.next_level != "end":
            self.tilemap.next(self.next_level)
        else:
            self.tilemap.end()

    def blit(self, cord=None):
        self.check(self.player)
        if cord is None:
            self.screen.blit(self.image, self.position)
        else:
            self.screen.blit(self.image, (self.position[0] + cord[0], self.position[1] + cord[1]))

