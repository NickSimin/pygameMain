import pygame as pg


def load_music(path):
    music = pg.mixer.Sound("/pygameMain/game/data/" + path + ".wav")
    return music


def load_sfx(path):
    music = pg.mixer.Sound("/pygameMain/game/data/sfx/" + path + ".wav")
    return music
