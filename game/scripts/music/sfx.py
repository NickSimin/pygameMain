import pygame as pg

from game.scripts.utilities.load.load_music import load_sfx
from game.scripts.music.music import Music


class Sfx(Music):

    def __init__(self, path):
        super().__init__("sfx/"+path)
