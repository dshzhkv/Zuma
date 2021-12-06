import math

import pygame
from Params import *


class Path:
    def __init__(self, level):
        self.step = 2
        self.nodes = []
        self.set_path(level)

    def set_path(self, level):
        if level == 1:
            self.set_square_path()
        elif level == 2:
            self.set_spiral_path()
        elif level == 3:
            self.set_triangle_path()

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

    def set_triangle_path(self):
        self.nodes += [(80, y) for y in range(0, HEIGHT - 81)]
        self.nodes += [(x, HEIGHT - 80) for x in range(80, WIDTH - 80)]

        line = [(x, 1.5 * x - HEIGHT + 160) for x in range(WIDTH - 80, 399,
                                                           -1)]
        self.nodes += line
        line.reverse()
        self.nodes += list(zip([x for x in range(400, 159, -1)],
                               [pos[1] for pos in line]))
        last_y = self.nodes[-1][1]
        self.nodes += [(x, last_y) for x in range(160, WIDTH - 241)]

    def set_spiral_path(self):
        radius = 18
        angle = 0.0

        x = int(radius * math.cos(angle))
        y = int(radius * math.sin(angle))
        nodes = [(x, y)]

        radius_step = radius
        angle_step = math.pi / 12

        for _ in range(9):
            angle += angle_step
            radius += radius_step
            x = int(radius * math.cos(angle))
            y = int(radius * math.sin(angle))
            nodes += [(x, y)]

        radius_step = 3
        for _ in range(50):
            angle += angle_step
            radius += radius_step
            x = int(radius * math.cos(angle))
            y = int(radius * math.sin(angle))
            nodes += [(x, y)]

        self.nodes += [(nodes[0][0] + WIDTH // 2 - 18, nodes[0][1] + HEIGHT // 2)]
        for i in range(0, len(nodes) - 1):
            start = (nodes[i][0] + WIDTH // 2 - 18, nodes[i][1] + HEIGHT // 2)
            end = (nodes[i + 1][0] + WIDTH // 2 - 18, nodes[i + 1][1] + HEIGHT // 2)

            self.nodes += [((start[0] + end[0]) / 2, (start[1] + end[1]) / 2), end]

        last_pos = self.nodes[-1]
        self.nodes += [(last_pos[0], y) for y in range(last_pos[1], -1, -self.step)]
        self.nodes.reverse()

    def draw(self, screen):
        for i in range(len(self.nodes) - 1):
            pygame.draw.line(screen, DARK_TAUPE, self.nodes[i],
                             self.nodes[i + 1], 10)
