import pygame as pg

from game.scripts.images.entities.entities import AnimateEntity
from game.scripts.utilities.load.load_image import load_images


class Player(AnimateEntity):
    def __init__(self, position, screen, fps, tilemap):
        self.position = position
        self.screen = screen

        self.cadres_idle = load_images("entities/player/idle")
        self.cadres_run = load_images("entities/player/run")

        self.slow_run = fps // len(self.cadres_run)
        self.slow_idle = fps // len(self.cadres_idle) * 3
        self.now_cadre_run = 0
        self.now_cadre_idle = 0

        for cadre in range(len(self.cadres_run)):
            self.cadres_run[cadre] = pg.transform.scale(self.cadres_run[cadre], (36, 42))
        for cadre in range(len(self.cadres_idle)):
            self.cadres_idle[cadre] = pg.transform.scale(self.cadres_idle[cadre], (36, 42))

        self.speed = [0, 0]
        self.SPEED = 3
        self.flipped = False
        self.tilemap = tilemap
        self.image = self.cadres_idle[0]

    def can_move(self):
        pos = self.position
        self.position = (pos[0] + self.speed[0], pos[1] + self.speed[1])
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return False
        self.position = pos
        return True

    def move(self):
        if self.can_move():
            self.tilemap.move((self.speed[0], self.speed[1]))

    def blit(self):
        if self.speed[0] != 0 and self.can_move():

            if self.speed[0] < 0 and not self.flipped:
                for cadre in range(len(self.cadres_run)):
                    self.cadres_run[cadre] = pg.transform.flip(self.cadres_run[cadre], True, False)
                for cadre in range(len(self.cadres_idle)):
                    self.cadres_idle[cadre] = pg.transform.flip(self.cadres_idle[cadre], True, False)

                self.flipped = True
            elif self.speed[0] > 0 and self.flipped:
                for cadre in range(len(self.cadres_run)):
                    self.cadres_run[cadre] = pg.transform.flip(self.cadres_run[cadre], True, False)
                for cadre in range(len(self.cadres_idle)):
                    self.cadres_idle[cadre] = pg.transform.flip(self.cadres_idle[cadre], True, False)

                self.flipped = False
            self.screen.blit(self.cadres_run[self.now_cadre_run // self.slow_run % len(self.cadres_run)], self.position)
            self.now_cadre_run += 1
            self.now_cadre_idle = 0
            self.move()
        else:
            self.screen.blit(self.cadres_idle[self.now_cadre_idle // self.slow_idle % len(self.cadres_idle)],
                             self.position)
            self.now_cadre_idle += 1
            self.now_cadre_run = 0
