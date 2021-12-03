import pygame
from Params import *


class Path:
    def __init__(self, form='square'):
        self.start = (0, 80)
        self.end = (160, 340)
        self.step = 2
        self.nodes = []
        self.set_path(form)

    def set_path(self, level):
        if level == 1:
            self.set_square_path()
        elif level == 2:
            self.set_square_path()

    def set_square_path(self):
        self.nodes += [(i, 80) for i in
                       range(0, WIDTH - 79, self.step)]  # right
        self.nodes += [(WIDTH - 80, i) for i in
                       range(80, HEIGHT - 79, self.step)]  # down
        self.nodes += [(i, HEIGHT - 80) for i in
                       range(WIDTH - 80, 79, -self.step)]  # left
        self.nodes += [(80, i) for i in
                       range(HEIGHT - 80, 139, -self.step)]  # up
        self.nodes += [(i, 140) for i in range(80, WIDTH - 159, self.step)]
        self.nodes += [(WIDTH - 160, i) for i in
                       range(140, HEIGHT - 159, self.step)]
        self.nodes += [(i, HEIGHT - 160) for i in
                       range(WIDTH - 160, 159, -self.step)]
        self.nodes += [(160, i) for i in range(HEIGHT - 160, 339, -self.step)]

    def set_circle_path(self):
        self.nodes += [(i, 80) for i in
                       range(0, WIDTH // 2, self.step)]
        last_x = self.nodes[-1][0]
        self.nodes += [(last_x + 2, 81), (last_x + 4, 82), (last_x + 6, 83), (last_x + 8, 84)]

    def draw(self, screen):
        for i in range(len(self.nodes) - 1):
            pygame.draw.line(screen, DARK_TAUPE, self.nodes[i], self.nodes[i + 1],
                             10)
