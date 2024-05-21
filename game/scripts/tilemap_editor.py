import pygame as pg

from game.scripts.images.image import Background
from game.scripts.images.button import Button
from game.scripts.images.entities.player import Player
from game.scripts.tilemap.tilemap import TileMap
from game.scripts.tilemap.tile import Tile
from game.scripts.utilities.json.load_json_tilemap import LoadJsonTilemap
from game.scripts.music.music import Music
from game.scripts.music.sfx import Sfx
from game.scripts.text.dialog.dialog import Dialog

pg.init()


class Editor:
    def __init__(self, size_window, fps):
        self.screen = pg.display.set_mode(size_window)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.is_run = True
        self.is_run_main_menu = True
        self.background = Background("Background", self.screen, size_window)
        self.tilemap = TileMap("editor_map", 32, size_window, self.screen, self.fps)

        self.SPEED = 3

        self.types = {"spawners": 2, "grass": 9, "stone": 9}
        self.keys_types = list(self.types.keys())
        self.now_key = 0
        self.now_variant = 0
        self.tile = Tile(self.keys_types[self.now_key], self.now_variant, (0, 0), self.screen, 32)
        self.tile.set_opacity(200)

        self.position = [0, 0]

    def run(self):
        while self.is_run and self.is_run_main_menu:
            keys = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4 and keys[pg.K_LSHIFT]:
                        self.now_key = (self.now_key + 1) % len(self.keys_types)
                        self.now_variant = 0
                    if event.button == 5 and keys[pg.K_LSHIFT]:
                        self.now_key = (self.now_key - 1) % len(self.keys_types)
                        self.now_variant = 0

                    if event.button == 4 and not keys[pg.K_LSHIFT]:
                        self.now_variant = (self.now_variant + 1) % self.types[self.keys_types[self.now_key]]
                    if event.button == 5 and not keys[pg.K_LSHIFT]:
                        self.now_variant = (self.now_variant - 1) % self.types[self.keys_types[self.now_key]]

                    if event.button == 1:

                        position = ((pg.mouse.get_pos()[0] + self.position[0]) // 32,\
                                        (pg.mouse.get_pos()[1] + self.position[1]) // 32)
                        position = str(position[0]) + ";" + str(position[1])
                        self.tilemap.editor_add_tile(position, self.keys_types[self.now_key], self.now_variant)
                        self.tilemap.editor_update()
                    if event.button == 3:
                        self.tilemap.editor_remove_tile(((pg.mouse.get_pos()[0] + self.position[0]) // 32,\
                                                        (pg.mouse.get_pos()[1] + self.position[1]) // 32))
                        self.tilemap.editor_update()
            self.tile.set_image(self.keys_types[self.now_key], self.now_variant)
            if keys[pg.K_a]:
                self.tilemap.editor_move((-self.SPEED, 0))
                self.position[0] -= self.SPEED
            if keys[pg.K_d]:
                self.tilemap.editor_move((self.SPEED, 0))
                self.position[0] += self.SPEED
            if keys[pg.K_s]:
                self.tilemap.editor_move((0, self.SPEED))
                self.position[1] += self.SPEED
            if keys[pg.K_w]:
                self.tilemap.editor_move((0, -self.SPEED))
                self.position[1] -= self.SPEED
            if keys[pg.K_q]:
                self.tilemap.editor_save()

            self.clock.tick(self.fps)

            self.background.blit()
            self.tilemap.editor_blit()
            self.tile.blit()

            pg.display.flip()


editor = Editor((800, 600), 60)
editor.run()

