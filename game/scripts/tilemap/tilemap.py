import pygame as pg
import json

from game.scripts.tilemap.tile import Tile
from game.scripts.utilities.json.load_json_tilemap import LoadJsonTilemap
from game.scripts.images.entities.player import Player


class TileMap:
    def __init__(self, path, tilesize, size, screen, fps):
        tilemap = LoadJsonTilemap("/pygameMain/game/data/maps/" + path)
        self.tilemap = {}
        self.tilesize = tilesize
        self.position = (0, 0)
        self.size = size
        self.screen = screen
        self.fps = fps
        for cord, tile in tilemap.items():
            now_cord = cord.split(";")
            position = (int(now_cord[0]) * self.tilesize, int(now_cord[1]) * self.tilesize)
            if tile["type"] != "spawners":
                self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)
            elif tile["variant"] == 0:

                self.player = Player((position[0] - 12, position[1] - 12), self.screen, self.fps, self)

    def move(self, speed):
        for cord, tile in self.tilemap.items():
            tile.position = (tile.position[0] - speed[0], tile.position[1] - speed[1])

    def blit(self):
        for cord, tile in self.tilemap.items():

            tile.blit()
