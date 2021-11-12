import pygame
import math
from enum import Enum
from Params import *


class Direction(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, center, path):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.image = pygame.Surface(BALL_SIZE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=center)

        self.direction = Direction.Right
        self.path = path

    def update(self):
        self.move()
        self.change_direction()

    def move(self):
        if self.direction == Direction.Right:
            self.rect.center = (self.rect.center[0] + 5, self.rect.center[1])
        elif self.direction == Direction.Down:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + 5)
        elif self.direction == Direction.Left:
            self.rect.center = (self.rect.center[0] - 5, self.rect.center[1])
        else:
            self.rect.center = (self.rect.center[0], self.rect.center[1] - 5)

    def change_direction(self):
        if self.rect.center in self.path:
            if self.direction == Direction.Up:
                self.direction = Direction.Right
            else:
                self.direction = Direction(self.direction.value + 1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.smoothscale(
            pygame.image.load("original.png"), TURTLE_SIZE)
        self.original_image.set_colorkey(BLACK)

        self.image = self.original_image

        self.rect = self.image.get_rect(center=SCREEN_CENTRE)

        self.angle = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)