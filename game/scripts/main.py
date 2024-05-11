import pygame as pg

from game.scripts.images.image import Image
from game.scripts.images.image import Background
from game.scripts.images.button import Button
from game.scripts.images.entities.player import Player
pg.init()


class Game:
    def __init__(self, size_window, fps, caption):
        self.screen = pg.display.set_mode(size_window)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.is_run = True
        self.is_run_main_menu = True
        self.background = Background("background", self.screen, size_window)
        self.main_menu_button = Button((size_window[0]//2, size_window[1]//2), self.screen, "Play")

        self.player = Player((size_window[0]//2, size_window[1]//2), self.screen, fps)
        pg.display.set_caption(caption)

    def menu(self):
        while self.is_run and self.is_run_main_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
            self.clock.tick(self.fps)

            self.background.blit()
            self.main_menu_button.blit()

            if self.main_menu_button.is_mouse_click():
                self.is_run_main_menu = False

            pg.display.flip()

    def run(self):
        while self.is_run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False

            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.player.speed[0] = -self.player.SPEED
            elif keys[pg.K_d]:
                self.player.speed[0] = self.player.SPEED
            else:
                self.player.speed[0] = 0

            self.clock.tick(self.fps)

            self.background.blit()
            self.player.blit()
            pg.display.flip()


game = Game((1024, 512), 60, "Game")
game.menu()
game.run()

pg.quit()
