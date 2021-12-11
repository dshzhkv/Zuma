import math

import pygame
from Params import *


class Path:
    def __init__(self, level):
        self.positions = []
        self.targets = []
        self.step = 2
        self.set_path(level)

    def set_path(self, level):
        if level == 1:
            self.set_triangle_path()
        elif level == 2:
            self.set_spiral_path()
        elif level == 3:
            self.set_square_path()

    def set_square_path(self):
        self.targets = [(0, 80), (WIDTH - 80, 80), (WIDTH - 80, HEIGHT - 80),
                   (80, HEIGHT - 80), (80, 140), (WIDTH - 160, 140),
                   (WIDTH - 160, HEIGHT - 160), (160, HEIGHT - 160),
                   (160, 340)]
        self.set_positions()

    def set_triangle_path(self):
        self.targets = [(80, 0), (80, HEIGHT - 80), (WIDTH - 80, HEIGHT - 80),
                        (400, 80), (160, 460), (WIDTH - 280, 460)]
        self.set_positions()

    def set_spiral_path(self):
        self.targets = [(64, 0), (64, 416), (99, 492), (153, 559), (222, 607),
                        (301, 637), (382, 645), (461, 631), (536, 597),
                        (598, 546), (644, 481), (671, 406), (679, 330),
                        (665, 254), (634, 186), (586, 128), (524, 84),
                        (454, 58), (383, 51), (312, 64), (246, 94), (193, 140),
                        (151, 198), (127, 262), (121, 331), (133, 396),
                        (162, 458), (204, 508), (259, 546), (319, 567),
                        (383, 573), (444, 561), (500, 535), (547, 495),
                        (583, 444), (602, 389), (607, 330), (596, 273),
                        (571, 220), (534, 178), (488, 146), (435, 128),
                        (382, 123), (330, 133), (282, 156), (242, 190),
                        (214, 233), (197, 281), (193, 330), (203, 377),
                        (224, 421), (255, 457), (303, 470), (345, 469),
                        (383, 456), (409, 434), (427, 407), (432, 380),
                        (428, 356), (417, 340), (339, 330)]
        self.set_positions()

    def set_positions(self):
        pos = pygame.math.Vector2(self.targets[0])
        direction = pygame.math.Vector2((0, 0))

        target_index = 0

        while target_index < len(self.targets):
            pos = pos + (direction * self.step)
            self.positions.append(pos)

            if (round(pos.x), round(pos.y)) == self.targets[target_index]:
                target_index += 1
                if target_index == len(self.targets):
                    break
                direction = self.change_direction(target_index, pos)

    def change_direction(self, target_index, pos):
        direction = pygame.math.Vector2(
            (self.targets[target_index][0] - pos[0],
             self.targets[target_index][1] - pos[1]))
        length = math.hypot(*direction)
        direction = pygame.math.Vector2(
            (direction[0] / length,
             direction[1] / length))
        return direction

    def draw(self, screen):
        for i in range(len(self.targets) - 1):
            pygame.draw.line(screen, DARK_TAUPE, self.targets[i],
                             self.targets[i + 1], 10)
