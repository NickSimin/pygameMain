import pygame as pg
from game.scripts.images.image import Image


class Tile(Image):
    def __init__(self, path, variant, position, screen, tilesize):
        super().__init__("tiles/" + path + "/" + str(variant), position, screen)
        self.tilesize = tilesize
        self.image = pg.transform.scale(self.image, (self.tilesize, self.tilesize))
        self.rect = self.image.get_rect()
        self.variant = variant

    def blit(self):
        self.screen.blit(self.image, self.position)
        #pg.draw.rect(self.screen, (255, 0, 0), (self.position[0], self.position[1], self.tilesize, self.tilesize), 1)