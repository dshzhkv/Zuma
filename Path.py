import pygame
from Params import *


class Path:
    def __init__(self):
        self.start = (0, 80)
        self.end = (160, 340)
        self.nodes = []
        self.set_path()

    def set_path(self):
        self.nodes += [(i, 80) for i in range(0, WIDTH - 79, 5)]  # right
        self.nodes += [(WIDTH - 80, i) for i in range(80, HEIGHT - 79, 5)]  # down
        self.nodes += [(i, HEIGHT - 80) for i in range(WIDTH - 80, 79, -5)]  # left
        self.nodes += [(80, i) for i in range(HEIGHT - 80, 139, -5)]  # up
        self.nodes += [(i, 140) for i in range(80, WIDTH - 159, 5)]
        self.nodes += [(WIDTH - 160, i) for i in range(140, HEIGHT - 159, 5)]
        self.nodes += [(i, HEIGHT - 160) for i in range(WIDTH - 160, 159, -5)]
        self.nodes += [(160, i) for i in range(HEIGHT - 160, 339, -5)]

    def draw(self, screen):
        for i in range(len(self.nodes) - 1):
            pygame.draw.line(screen, WHITE, self.nodes[i], self.nodes[i + 1],
                             10)
