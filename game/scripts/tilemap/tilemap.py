import pygame as pg
import json

from game.scripts.tilemap.tile import Tile
from game.scripts.utilities.json.load_json_tilemap import LoadJsonTilemap
from game.scripts.images.entities.player import Player
from game.scripts.images.entities.exit import Exit
from game.scripts.images.entities.table import Table

from game.scripts.text.dialog.dialog import Dialog


class TileMap:
    def __init__(self, path, tilesize, size, screen, fps, play):
        self.exit = None
        self.dialog = None
        self.utilities_tilemap = LoadJsonTilemap("/pygameMain/game/data/maps/" + path)
        self.tilesize = tilesize
        self.position = [0, 0]
        self.size = size
        self.screen = screen
        self.fps = fps
        self.tilemap = {}
        self.entities = {}
        self.player = None
        self.load()
        self.play = play

    def load(self):
        self.tilemap = {}
        self.entities = {}
        self.dialog = None
        self.player = None
        for cord, tile in self.utilities_tilemap.items():
            if cord == "dialog":

                self.dialog = Dialog(tile, self.screen)
                self.dialog.is_visible = True
                continue
            now_cord = cord.split(";")

            position = (int(now_cord[0]) * self.tilesize, int(now_cord[1]) * self.tilesize)
            if tile["type"] != "spawners":
                self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)
            elif tile["variant"] == 0:

                self.player = Player((position[0] - 12, position[1] - 12), self.screen, self.fps, self)
                self.entities[position] = self.player
                self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)
            elif tile["variant"] == 1:
                if tile.get("next") is not None:
                    self.exit = Exit(position, self.screen, tile["next"], self, self.player)
                else:
                    self.exit = Exit(position, self.screen, "0", self, self.player)
                self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)

    def move(self, speed):

        for cord, tile in self.tilemap.items():
            tile.position = (tile.position[0] - speed[0], tile.position[1] - speed[1])
        if self.exit is not None:
            self.exit.position = (self.exit.position[0] - speed[0], self.exit.position[1] - speed[1])

    def _move(self, speed):
        self.position[0] -= speed[0]
        self.position[1] -= speed[1]
        # for cord, tile in self.tilemap.items():
        #     tile.position = (tile.position[0] - speed[0], tile.position[1] - speed[1])

    def editor_move(self, speed):
        self._move(speed)
        # for cord, entity in self.entities.items():
        #     entity.editor_position = (entity.editor_position[0] - speed[0], entity.editor_position[1] - speed[1])

    def blit(self, is_editor=False):

        if self.exit is not None and not is_editor:
            self.exit.check(self.player)
            pg.draw.rect(self.screen, (255, 0, 0), (self.exit.position[0], self.exit.position[1], \
                                                    self.exit.size[0], self.exit.size[1]), 1)

        print(self.player.position)
        for cord, tile in self.tilemap.items():
            if (tile.type_tile == "spawners" or tile.type_tile == "exit") and not is_editor:
                continue

            tile.blit(self.position)

            # if self.exit is not None:
            #     self.exit.blit()

        if self.exit is not None:
            self.exit.blit()
        if self.dialog is not None:
            self.dialog.blit()


    def editor_blit(self):
        self.blit(True)

    def editor_save(self):
        self.utilities_tilemap.save()

    def editor_add_tile(self, position, type_tile, variant):
        self.utilities_tilemap.add_tile(position, type_tile, variant)

    def editor_remove_tile(self, position):
        pos = str(position[0]) + ";" + str(position[1])
        self.utilities_tilemap.remove_tile(pos)

    def editor_update(self):
        self.load()

    def next(self, next_path):
        self.utilities_tilemap = LoadJsonTilemap("/pygameMain/game/data/maps/" + next_path)
        self.load()
        self.play.update_player()

    def end(self):
        self.play.end()

