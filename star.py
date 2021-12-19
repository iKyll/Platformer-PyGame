import pygame
import sys
import os

class Star(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(sys.path[0], "assets\\projectile.png")), (75,75))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)