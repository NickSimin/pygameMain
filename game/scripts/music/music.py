import pygame as pg

from game.scripts.utilities.load.load_music import load_music


class Music:
    def __init__(self, path):
        self.path = path
        self.music = load_music(self.path)


    def play(self):
        self.music.play()

    def stop(self):
        self.music.stop()

    def pause(self):
        self.music.pause()