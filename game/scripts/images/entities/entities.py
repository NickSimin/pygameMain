from game.scripts.images.image import Image
from game.scripts.utilities.load.load_image import load_images


class Entity(Image):
    def __init__(self, path, position, screen):
        super().__init__(path, position, screen)
        self.editor_position = position

    def blit(self, cord=None):
        if cord is None:
            self.screen.blit(self.image, self.position)
        else:
            self.screen.blit(self.image, (self.position[0] + cord[0], self.position[1] + cord[1]))

    def editor_blit(self):
        self.screen.blit(self.image, self.editor_position)


class AnimateEntity(Entity):
    def __init__(self, path, position, screen, fps):
        self.position = position
        self.editor_position = position
        self.screen = screen
        self.cadres = load_images(path)
        self.FPS = fps
        self.slow = fps//len(self.cadres)
        self.now_cadre = 0
        self.image = self.cadres[0]

    def blit(self, cord=None):
        if cord is None:
            self.screen.blit(self.cadres[self.now_cadre // self.slow], self.position)

        else:
            self.screen.blit(self.cadres[self.now_cadre // self.slow], (self.position[0] + cord[0], self.position[1] + cord[1]))
        self.now_cadre += 1
        if self.now_cadre >= len(self.cadres):
            self.now_cadre = 0

    def editor_blit(self):
        self.screen.blit(self.image, self.editor_position)
