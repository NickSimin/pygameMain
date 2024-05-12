import pygame as pg

from game.scripts.images.entities.entities import AnimateEntity
from game.scripts.utilities.load.load_image import load_images


class Player(AnimateEntity):
    def __init__(self, position, screen, fps, tilemap):
        self.position = position
        self.screen = screen

        self.cadres_idle = load_images("entities/player/idle")
        self.cadres_run = load_images("entities/player/run")
        self.cadres_jump = load_images("entities/player/jump")

        self.slow_jump = fps // len(self.cadres_run)
        self.slow_run = fps // len(self.cadres_run)
        self.slow_idle = fps // len(self.cadres_idle) * 3

        self.now_cadre_run = 0
        self.now_cadre_idle = 0
        self.now_cadre_jump = 0

        for cadre in range(len(self.cadres_run)):
            self.cadres_run[cadre] = pg.transform.scale(self.cadres_run[cadre], (36, 42))
        for cadre in range(len(self.cadres_idle)):
            self.cadres_idle[cadre] = pg.transform.scale(self.cadres_idle[cadre], (36, 42))

        for cadre in range(len(self.cadres_jump)):
            self.cadres_jump[cadre] = pg.transform.scale(self.cadres_jump[cadre], (36, 42))

        self.speed = [0, 0]
        self.SPEED = 3
        self.FPS = fps
        self.is_flip = False

        self.is_jump = False
        self.is_start_jump = False

        self.jump_timer = 0
        self.tilemap = tilemap
        self.image = self.cadres_idle[0]

    def can_move(self):
        pos = self.position
        self.position = (pos[0] + self.speed[0], pos[1] + self.speed[1] - self.tilemap.tilesize // 4)
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return False
        self.position = pos
        return True

    def physics(self):
        if self.is_jump:
            return False
        pos = self.position
        self.position = (pos[0], pos[1] + self.tilemap.tilesize // 2)
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return False
        self.position = pos
        return True

    def is_stand(self):
        pos = self.position
        self.position = (pos[0], pos[1] + self.tilemap.tilesize // 8)
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return True
        self.position = pos
        return False

    def move_horisontal(self):
        if self.can_move():
            self.tilemap.move((self.speed[0], 0))
    def flip(self):
        for cadre in range(len(self.cadres_run)):
            self.cadres_run[cadre] = pg.transform.flip(self.cadres_run[cadre], True, False)
        for cadre in range(len(self.cadres_idle)):
            self.cadres_idle[cadre] = pg.transform.flip(self.cadres_idle[cadre], True, False)
        for cadre in range(len(self.cadres_jump)):
            self.cadres_jump[cadre] = pg.transform.flip(self.cadres_jump[cadre], True, False)

        self.is_flip = not self.is_flip
    def blit(self):
        if self.is_jump:
            self._jump()
        if self.speed[0] != 0 and self.can_move():

            if self.speed[0] < 0 and not self.is_flip:
                self.flip()
            elif self.speed[0] > 0 and self.is_flip:
                self.flip()
            if not self.is_start_jump:
                self.screen.blit(self.cadres_run[self.now_cadre_run // self.slow_run % len(self.cadres_run)], self.position)
                self.now_cadre_run += 1
            self.now_cadre_idle = 0
            self.move_horisontal()
        else:
            if not self.is_start_jump:

                self.screen.blit(self.cadres_idle[self.now_cadre_idle // self.slow_idle % len(self.cadres_idle)],
                             self.position)
                self.now_cadre_idle += 1
            self.now_cadre_run = 0

        if self.speed[1] > 0:
            if not self.is_stand():
                self.tilemap.move((0, self.SPEED))

        elif self.speed[1] < 0:
            self.tilemap.move((0, -self.SPEED))
        if self.physics():
            self.speed[1] = 10

        '''print(self.speed[1])'''

    def _jump(self):
        self.jump_timer += 1
        if self.jump_timer < self.FPS // 2:
            if self.jump_timer < self.FPS // 4:
                if self.speed[0] < 0 and not self.is_flip:
                    self.flip()
                elif self.speed[0] > 0 and self.is_flip:
                    self.flip()

                self.screen.blit(self.cadres_jump[self.now_cadre_jump // self.slow_jump % len(self.cadres_jump)],
                                 self.position)
                self.now_cadre_jump += 1
                self.is_start_jump = True
            else:
                self.is_start_jump = False
            self.speed[1] = -self.FPS / self.jump_timer

        elif self.jump_timer < self.FPS:
            self.is_start_jump = False
            if not self.is_stand():
                self.speed[1] = self.FPS / self.jump_timer
        else:
            self.jump_timer = 0
            self.speed[1] = 0
            self.is_jump = False
            self.is_start_jump = 0

    def start_jump(self):
        if self.is_stand():
            self.is_jump = True
            self.jump_timer = 0
