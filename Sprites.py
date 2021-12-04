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
    def __init__(self, color, center, path):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.direction = Direction.Right
        self.path = path
        self.pos_in_path = self.path.nodes.index(center)

        self.image = pygame.Surface(BALL_SIZE)
        self.rect = self.image.get_rect(center=center)

        self.can_move = True

    def update(self):
        if self.can_move:
            self.move(1)

    def move(self, steps):
        self.pos_in_path += steps
        self.rect.center = self.path.nodes[self.pos_in_path]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)

    def __eq__(self, other):
        return self.color == other.color and \
               self.rect.center == other.rect.center and \
               self.can_move == other.can_move


class ShootingBall(pygame.sprite.Sprite):
    def __init__(self, color, pos=SCREEN_CENTER):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.image = pygame.Surface(BALL_SIZE)
        self.rect = self.image.get_rect(center=pos)

        self.target = (0, 0)
        self.speed = 15

    def set_target(self, target):
        self.target = (target[0] - self.rect.center[0],
                       target[1] - self.rect.center[1])
        length = math.hypot(*self.target)
        self.target = (self.target[0] / length, self.target[1] / length)
        # self.angle = math.degrees(math.atan2(-self.target[1], self.target[0]))

    def update(self):
        self.rect.center = (self.rect.center[0] + self.target[0] * self.speed,
                            self.rect.center[1] + self.target[1] * self.speed)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos=SCREEN_CENTER):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos

        self.original_image = pygame.transform.smoothscale(
            pygame.image.load("original.png"), PLAYER_SIZE)
        self.original_image.set_colorkey(BLACK)

        self.image = self.original_image

        self.rect = self.image.get_rect(center=pos)

        self.angle = 0

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Finish(pygame.sprite.Sprite):
    def __init__(self, path, balls):
        pygame.sprite.Sprite.__init__(self)

        self.balls = balls

        self.is_finished = False

        self.image = pygame.transform.smoothscale(
            pygame.image.load("star.png"), (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=path.nodes[-1])

    def update(self):
        for ball in self.balls:
            if self.rect.colliderect(ball.rect):
                self.is_finished = True
                break

    def draw(self, screen):

        screen.blit(self.image, (self.rect.x, self.rect.y))