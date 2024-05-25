import pygame as pg

from game.scripts.images.image import Background
from game.scripts.images.button import Button
from game.scripts.images.entities.player import Player
from game.scripts.tilemap.tilemap import TileMap
from game.scripts.music.music import Music

from game.scripts.music.sfx import Sfx
from game.scripts.text.dialog.dialog import Dialog
from game.scripts.text.text import Text
pg.init()


class Game:
    def __init__(self, size_window, fps, caption, level):
        self.screen = pg.display.set_mode(size_window)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.is_run = True
        self.is_run_main_menu = True
        self.background = Background("Background", self.screen, size_window)
        self.main_menu_button = Button((size_window[0] // 2, size_window[1] // 2), self.screen, "Play")

        self.tilemap = TileMap(level, 32, size_window, self.screen, self.fps, self)
        self.player = self.tilemap.player

        self.main_music = Music("music")

        self.main_music.play()

        pg.display.set_caption(caption)

        self.end_text = Text("Поздравляем Вас, Вы вышли из симуляции.", 24,\
                             (size_window[0] // 4, size_window[1] // 2), (255, 255, 255), self.screen)

    def menu(self):
        while self.is_run and self.is_run_main_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
            self.clock.tick(self.fps)

            self.background.blit()
            self.main_menu_button.blit()

            if self.main_menu_button.is_mouse_click_button():
                self.is_run_main_menu = False

            pg.display.flip()

    def run(self):
        while self.is_run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False

            keys = pg.key.get_pressed()
            if keys[pg.K_f]:
                self.player.start_dash()
            elif keys[pg.K_a]:
                self.player.set_speed(False)
            elif keys[pg.K_d]:
                self.player.set_speed(True)
            else:
                self.player.speed[0] = 0
            if keys[pg.K_SPACE]:
                self.player.start_jump()

            if self.player.fall_timer > self.fps * 2:
                self.end()

            self.clock.tick(self.fps)

            self.background.blit()
            self.tilemap.blit()
            self.player.blit()
            print(self.player.position)

            pg.display.flip()

    def end(self):
        while self.is_run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
            self.clock.tick(self.fps)

            self.background.blit()
            self.end_text.blit()

            pg.display.flip()

    def update_player(self):
        self.player = self.tilemap.player

game = Game((1024, 512), 60, "Simulate", "0")
game.menu()
game.run()

pg.quit()
