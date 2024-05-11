import pygame as pg
from os import listdir


def load_image(path, is_png=True):
    if is_png:
        image = pg.image.load("/pygameMain/game/data/images/" + path + ".png").convert()
    else:
        image = pg.image.load("/pygameMain/game/data/images/" + path).convert()
    image.set_colorkey((0, 0, 0))
    return image
def load_images(path):
    images = []

    for image in listdir("/pygameMain/game/data/images/" + path):
        images.append(load_image(path + "/" + image, False))

    return images
