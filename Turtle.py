import math
import pygame
from Params import *


class Turtle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.smoothscale(
            pygame.image.load("original.png"), (100, 100))
        self.original_image.set_colorkey(BLACK)

        self.image = self.original_image

        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        self.angle = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
