import pygame
from Params import *


class Path:
    def __init__(self):
        self.nodes = [(0, 80), (WIDTH - 80, 80), (WIDTH - 80, HEIGHT - 80),
                      (80, HEIGHT - 80), (80, 140), (WIDTH - 160, 140),
                      (WIDTH - 160, HEIGHT - 160), (160, HEIGHT - 160), (160,
                                                                         340)]

    def draw(self, screen):
        for i in range(len(self.nodes) - 1):
            pygame.draw.line(screen, WHITE, self.nodes[i], self.nodes[i + 1],
                             10)