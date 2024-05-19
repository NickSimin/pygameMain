import pygame as pg
import json


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
