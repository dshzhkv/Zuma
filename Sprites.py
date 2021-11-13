import pygame
import random
import math
from enum import Enum
from Params import *


class Direction(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, path):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.direction = Direction.Right
        self.speed = 5
        self.path = path

        self.image = pygame.Surface(BALL_SIZE)
        self.rect = self.image.get_rect(center=self.path.start)

    def update(self):
        self.move()
        self.change_direction()

    def move(self):
        if self.direction == Direction.Right:
            self.rect.center = (self.rect.center[0] + self.speed,
                                self.rect.center[1])
        elif self.direction == Direction.Down:
            self.rect.center = (self.rect.center[0],
                                self.rect.center[1] + self.speed)
        elif self.direction == Direction.Left:
            self.rect.center = (self.rect.center[0] - self.speed,
                                self.rect.center[1])
        else:
            self.rect.center = (self.rect.center[0],
                                self.rect.center[1] - self.speed)

    def change_direction(self):
        if self.rect.center in self.path.nodes:
            if self.direction == Direction.Up:
                self.direction = Direction.Right
            else:
                self.direction = Direction(self.direction.value + 1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)


class ShootingBall(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.image = pygame.Surface(BALL_SIZE)
        self.rect = self.image.get_rect(center=SCREEN_CENTER)

        self.target = (0, 0)
        self.angle = 0
        self.speed = 10

    def set_target(self, target):
        self.target = (target[0] - self.rect.center[0],
                       target[1] - self.rect.center[1])
        length = math.hypot(*self.target)
        self.target = (self.target[0] / length, self.target[1] / length)
        self.angle = math.degrees(math.atan2(-self.target[1], self.target[0]))

    def update(self):
        self.rect.center = (self.rect.center[0] + self.target[0] * self.speed,
                            self.rect.center[1] + self.target[1] * self.speed)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = pygame.transform.smoothscale(
            pygame.image.load("original.png"), TURTLE_SIZE)
        self.original_image.set_colorkey(BLACK)

        self.image = self.original_image

        self.rect = self.image.get_rect(center=SCREEN_CENTER)

        self.angle = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
