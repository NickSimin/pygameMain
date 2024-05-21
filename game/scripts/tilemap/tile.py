import pygame as pg
from game.scripts.images.image import Image
from game.scripts.utilities.load.load_image import load_image


class Tile(Image):
    def __init__(self, path, variant, position, screen, tilesize):
        super().__init__("tiles/" + path + "/" + str(variant), position, screen)
        self.tilesize = tilesize
        self.image = pg.transform.scale(self.image, (self.tilesize, self.tilesize))
        self.rect = self.image.get_rect()
        self.variant = variant

    def blit(self, cord = None):
        if cord is None:
            self.screen.blit(self.image, self.position)
        else:
            self.screen.blit(self.image, (self.position[0] + cord[0], self.position[1] + cord[1]))

    def set_opacity(self, opacity):
        self.image.set_alpha(opacity)

    def set_image(self, path, variant):
        self.image = load_image("tiles/" + path + "/" + str(variant))
        self.image = pg.transform.scale(self.image, (self.tilesize, self.tilesize))
