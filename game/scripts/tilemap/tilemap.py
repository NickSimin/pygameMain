import pygame as pg
import json

from game.scripts.tilemap.tile import Tile
from game.scripts.utilities.json.load_json_tilemap import LoadJsonTilemap
from game.scripts.images.entities.player import Player


class TileMap:
    def __init__(self, path, tilesize, size, screen, fps):
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

    def load(self):
        self.tilemap = {}
        for cord, tile in self.utilities_tilemap.items():
            now_cord = cord.split(";")
            position = (int(now_cord[0]) * self.tilesize, int(now_cord[1]) * self.tilesize)
            if tile["type"] != "spawners":
                self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)
            elif tile["variant"] == 0:
                self.player = Player((position[0] - 12, position[1] - 12), self.screen, self.fps, self)
                self.entities[position] = self.player

    def move(self, speed):
        for cord, tile in self.tilemap.items():
            tile.position = (tile.position[0] - speed[0], tile.position[1] - speed[1])

    def _move(self, speed):
        self.position[0] -= speed[0]
        self.position[1] -= speed[1]
        # for cord, tile in self.tilemap.items():
        #     tile.position = (tile.position[0] - speed[0], tile.position[1] - speed[1])

    def editor_move(self, speed):
        self._move(speed)
        # for cord, entity in self.entities.items():
        #     entity.editor_position = (entity.editor_position[0] - speed[0], entity.editor_position[1] - speed[1])

    def blit(self):
        for cord, tile in self.tilemap.items():
            tile.blit(self.position)

    def editor_blit(self):
        self.blit()
        for cord, entity in self.entities.items():
            entity.blit(self.position)

    def editor_save(self):
        self.utilities_tilemap.save()

    def editor_add_tile(self, position, type_tile, variant):
        self.utilities_tilemap.add_tile(position, type_tile, variant)

    def editor_remove_tile(self, position):
        pos = str(position[0]) + ";" + str(position[1])
        self.utilities_tilemap.remove_tile(pos)

    def editor_update(self):
        self.load()


