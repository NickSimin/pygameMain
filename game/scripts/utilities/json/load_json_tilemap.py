import pygame as pg
import json
from game.scripts.utilities.json.load_json_dialog import LoadJsonDialog


class LoadJsonTilemap:
    def __init__(self, path):
        self.path = path + ".json"
        self.data = self.load()

    def load(self):
        with open(self.path) as file:
            data = json.load(file)
            return data

    def items(self):
        return self.data.items()

    def add_tile(self, position, type_tile, variant):
        self.data[position] = {"type": type_tile, "variant": variant}

    def remove_tile(self, position):
        if position in self.data:
            self.data.pop(position)
        else:
            print("error: tile not found")

    def save(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file)
