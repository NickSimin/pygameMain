import pygame as pg
from game.scripts.images.image import Image


class Tile(Image):
    def __init__(self, path, variant, position, screen, tilesize):
        super().__init__("tiles/" + path + "/" + str(variant), position, screen)
        self.tilesize = tilesize
        self.image = pg.transform.scale(self.image, (self.tilesize, self.tilesize))