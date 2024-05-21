import pygame as pg

from game.scripts.images.entities.entities import AnimateEntity
from game.scripts.utilities.load.load_image import load_images
from game.scripts.music.sfx import Sfx


class Player(AnimateEntity):
    def __init__(self, position, screen, fps, tilemap):
        self.position = position
        self.screen = screen

        self.cadres_idle = load_images("entities/player/idle")
        self.cadres_run = load_images("entities/player/run")
        self.cadres_jump = load_images("entities/player/jump")
        self.cadres_dash = load_images("entities/player/slide")
        self.cadres_jump_fall = load_images("entities/player/jump_fall")

        self.slow_jump = fps // len(self.cadres_run)
        self.slow_run = fps // len(self.cadres_run)
        self.slow_idle = fps // len(self.cadres_idle) * 3
        self.slow_dash = fps // len(self.cadres_dash)
        self.slow_jump_fall = fps // len(self.cadres_jump_fall)

        self.now_cadre_run = 0
        self.now_cadre_idle = 0
        self.now_cadre_jump = 0
        self.now_cadre_dash = 0
        self.now_cadre_jump_fall = 0

        self.SIZE = (60, 40)
        self.size = self.cadres_jump[0].get_size()
        for cadre in range(len(self.cadres_run)):
            self.cadres_run[cadre] = pg.transform.scale(self.cadres_run[cadre], self.SIZE)
        for cadre in range(len(self.cadres_idle)):
            self.cadres_idle[cadre] = pg.transform.scale(self.cadres_idle[cadre], self.SIZE)
        for cadre in range(len(self.cadres_jump)):
            self.cadres_jump[cadre] = pg.transform.scale(self.cadres_jump[cadre], self.SIZE)
        for cadre in range(len(self.cadres_dash)):
            self.cadres_dash[cadre] = pg.transform.scale(self.cadres_dash[cadre], self.SIZE)
        for cadre in range(len(self.cadres_jump_fall)):
            self.cadres_jump_fall[cadre] = pg.transform.scale(self.cadres_jump_fall[cadre], self.SIZE)

        self.speed = [1, 0]

        self.MAX_DASH_SPEED = [40, -2]
        self.dash_speed = [0, 0]
        self.SPEED = 3
        self.FPS = fps

        self.is_flip = False

        self.is_dash = False
        self.is_start_dash = False
        self.is_jump = False
        self.is_start_jump = False
        self.is_jump_physics = False

        self.is_fall = False

        self.jump_timer = 0
        self.dash_idle_timer = 0
        self.dash_timer = 0
        self.fall_timer = 0
        self.tilemap = tilemap
        self.image = self.cadres_idle[0]

        self.sfx_jump = Sfx("jump")
        self.sfx_dash = Sfx("dash")
        self.image = self.cadres_idle[0]
        self.editor_position = position

    def can_move(self):
        pos = self.position
        self.position = (pos[0] + self.speed[0], pos[1] - self.tilemap.tilesize)
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return False
        self.position = pos
        return True

    def can_dash(self):
        pos = self.position

        self.position = (pos[0] + self.dash_speed, pos[1] - self.tilemap.tilesize)

        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                print(cord)
                return False
        self.position = pos
        return True

    def physics(self):
        if self.is_jump_physics:
            return False
        pos = self.position
        self.position = (pos[0], pos[1] - self.tilemap.tilesize // 2)
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return False
        self.position = pos
        return True

    def is_stand(self):
        pos = self.position
        if self.is_flip:
            self.position = (pos[0], pos[1])
        else:
            self.position = (pos[0], pos[1])
        for cord, tile in self.tilemap.tilemap.items():
            if self.is_collide(tile):
                self.position = pos
                return True
        self.position = (pos[0], pos[1])
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
        for cadre in range(len(self.cadres_dash)):
            self.cadres_dash[cadre] = pg.transform.flip(self.cadres_dash[cadre], True, False)
        for cadre in range(len(self.cadres_jump_fall)):
            self.cadres_jump_fall[cadre] = pg.transform.flip(self.cadres_jump_fall[cadre], True, False)
        self.is_flip = not self.is_flip

    def blit(self, cord=None):
        if cord is None:
            self.dash_idle_timer += 1
            if self.is_jump:
                self._jump()
            if self.is_dash:
                self._dash()
            if self.speed[0] != 0 and self.can_move():

                if self.speed[0] < 0 and not self.is_flip:
                    self.flip()
                elif self.speed[0] > 0 and self.is_flip:
                    self.flip()
                if not self.is_dash and not self.is_fall and not self.is_jump:
                    self.screen.blit(self.cadres_run[self.now_cadre_run // self.slow_run % len(self.cadres_run)],
                                     self.position)
                    self.now_cadre_run += 1
                self.now_cadre_idle = 0
                self.move_horisontal()
            else:
                if not self.is_dash and not self.is_fall and not self.is_jump:
                    self.screen.blit(self.cadres_idle[self.now_cadre_idle // self.slow_idle % len(self.cadres_idle)],
                                     self.position)
                    self.now_cadre_idle += 1
                self.now_cadre_run = 0

            if self.speed[1] > 0:
                if not self.is_stand():
                    self.tilemap.move((0, self.SPEED))
                    if self.speed[0] < 0 and not self.is_flip:
                        self.flip()
                    elif self.speed[0] > 0 and self.is_flip:
                        self.flip()
                    self.screen.blit(self.cadres_jump_fall[self.now_cadre_jump_fall // self.slow_jump_fall \
                                                           % len(self.cadres_jump_fall)], self.position)
                    self.now_cadre_jump_fall += 1
                    self.is_fall = True
                    self.fall_timer += 1
                else:
                    self.fall_timer = 0
                    self.is_fall = False
            if self.is_jump:
                self.tilemap.move((0, self.speed[1]))
            if self.physics() and not self.is_jump_physics:
                self.speed[1] = 1
                self.tilemap.move((0, self.speed[1]))
            # pg.draw.rect(self.screen, (255, 0, 0), (self.position[0], self.position[1], self.size[0], \
            #                                         self.size[1]), 1)
        else:
            self.screen.blit(self.image, (self.position[0] + cord[0], self.position[1] + cord[1]))

    def _jump(self):
        self.jump_timer += 1

        if self.jump_timer < self.FPS // 3:
            if self.speed[0] < 0 and not self.is_flip:
                self.flip()
            elif self.speed[0] > 0 and self.is_flip:
                self.flip()
            self.screen.blit(self.cadres_jump[self.now_cadre_jump // self.slow_jump % len(self.cadres_jump)],
                             self.position)
            self.now_cadre_jump += 1
            self.speed[1] = -3
        elif self.jump_timer < self.FPS * 2 // 3:
            self.screen.blit(self.cadres_jump[self.now_cadre_jump // self.slow_jump % len(self.cadres_jump)],
                             self.position)
            self.now_cadre_jump += 1
            self.is_jump_physics = False
        else:
            self.is_jump_physics = False
            self.jump_timer = 0
            self.speed[1] = 0
            self.is_jump = False
            self.is_start_jump = 0
            self.sfx_jump.stop()

    def start_jump(self):
        if self.is_stand() and not self.is_jump and not self.is_dash and not self.is_fall:
            self.is_jump = True
            self.is_jump_physics = True
            self.jump_timer = 0
            self.sfx_jump.play()

    def _dash(self):
        self.dash_timer += 1

        if self.is_dash:
            if not self.can_dash() or self.dash_timer >= self.FPS // 3 * 2:
                self.is_dash = False

            if self.dash_timer < self.FPS // 3 * 2:
                if self.is_flip:
                    self.dash_speed = -2
                else:
                    self.dash_speed = 2

                self.speed[0] = self.dash_speed

                self.screen.blit(self.cadres_dash[self.now_cadre_dash // self.slow_dash % len(self.cadres_dash)],
                                 self.position)
                self.now_cadre_dash += 1

        else:
            self.dash_speed = 0
            self.sfx_dash.stop()

    def start_dash(self):
        if not self.is_dash and self.dash_idle_timer >= self.FPS and not self.is_jump and not self.is_fall\
                and self.is_stand():
            self.is_start_dash = True
            self.is_dash = True
            self.dash_timer = 0
            self.dash_idle_timer = 0
            if self.is_flip:
                self.dash_speed = -2
            else:
                self.dash_speed = 2
            if self.can_dash():
                self.sfx_dash.play()
            self.dash_speed = 0

    def set_speed(self, is_flip):
        if is_flip and not self.is_flip:
            self.flip()
        elif not is_flip and self.is_flip:
            self.flip()
        if self.is_fall or (not self.is_stand() and not self.is_jump):
            return
        if is_flip:
            self.speed = [self.SPEED, 0]
        else:
            self.speed = [-self.SPEED, 0]
