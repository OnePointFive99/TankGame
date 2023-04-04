import pygame.image

from ParentObject import ParentObject


class Home(ParentObject):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('../Image/Home/Home.png')
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.isDestroy = False

    def draw(self, window):
        window.blit(self.image, self.rect)

