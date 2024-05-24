import pygame as pg
import json


class LoadJsonDialog:
    def __init__(self, path):

        self.path = "game/data/dialogs/" + path + ".json"
        self.data = self.load()

    def load(self):
        with open(self.path, encoding="utf-8") as file:
            data = json.load(file)
            return data

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def get_text(self, key):
        if not self.can_get_text(key):
            return None
        return self.data[key]["text"]

    def get_next(self, key):
        if not self.can_get_text(key):
            return None
        return self.data[key]["next"]

    def can_get_text(self, key):
        if key in self.data:
            return True
        else:
            return False

