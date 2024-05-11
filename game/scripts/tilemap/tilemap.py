import pygame as pg
import json

from game.scripts.tilemap.tile import Tile
from game.scripts.utilities.json.load_json_tilemap import LoadJsonTilemap


class TileMap:
    def __init__(self, path, tilesize, size, screen):
        tilemap = LoadJsonTilemap("/pygameMain/game/data/maps/" + path)
        self.tilemap = {}
        self.tilesize = tilesize
        self.position = (0, 0)
        self.size = size
        self.screen = screen
        for cord, tile in tilemap.items():
            now_cord = cord.split(";")
            position = (int(now_cord[0]) * self.tilesize, int(now_cord[1]) * self.tilesize)
            self.tilemap[position] = Tile(tile["type"], tile["variant"], position, self.screen, self.tilesize)

    def blit(self):
        for cord, tile in self.tilemap.items():
            if self.position[0] <= cord[0] < self.position[0] + self.size[0] and self.position[1] <= cord[1] \
                    < self.position[1] + self.size[1]:
                tile.blit()
