import pygame as pg
from game.scripts.images.entities.entities import Entity


class Exit(Entity):
    def __init__(self, position, screen, next_level):
        super().__init__("tiles/spawners/1", position, screen)
        self.next_level = next_level

    def next(self):
        pass
