from game.scripts.images.image import Image
from game.scripts.utilities.load.load_image import load_images


class Entity(Image):
    pass


class AnimateEntity(Entity):
    def __init__(self, path, position, screen, fps):
        self.position = position
        self.screen = screen
        self.cadres = load_images(path)
        self.FPS = fps
        self.slow = fps//len(self.cadres)
        self.now_cadre = 0
        self.image = self.cadres[0]

    def blit(self):
        self.screen.blit(self.cadres[self.now_cadre // self.slow], self.position)
        self.now_cadre += 1
        if self.now_cadre >= len(self.cadres):
            self.now_cadre = 0
