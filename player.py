import pygame
import os
import sys

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.jumps = 1
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_y_base = 5
        self.velocity = [0, 5]
        self.gravity = 1
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(sys.path[0], "assets\\alien.png")), (100,100))
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = 200


        