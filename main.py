import pygame
import random
import os
import math
from Params import *
from Path import *
from Sprites import *


class BallGenerator:
    def __init__(self, path, number):
        self.path = path
        self.colors = [BLUE, RED, GREEN, YELLOW]
        self.balls = []
        self.number = number

    def generate(self):
        if len(self.balls) < self.number:
            if len(self.balls) == 0:
                self.balls.append(Ball(random.choice(self.colors),
                                       self.path.start, self.path.nodes))
            if self.balls[-1].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.append(Ball(random.choice(self.colors),
                                       self.path.start, self.path.nodes))

    def update(self):
        for ball in self.balls:
            ball.update()
            if ball.rect.center == self.path.end:
                return False
        return True

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.path = Path()
        self.ball_generator = BallGenerator(self.path, 50)
        self.sprites = pygame.sprite.Group(self.player)

    def start(self):
        isRunning = True

        while isRunning:
            self.ball_generator.generate()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                isRunning = self.handle_event(event)

            isRunning = isRunning and self.update_sprites()
            self.update_display()

        pygame.quit()

    @staticmethod
    def handle_event(event):
        if event.type == pygame.QUIT:
            return False

        return True

    def update_sprites(self):
        self.sprites.update()
        return self.ball_generator.update()

    def update_display(self):
        self.screen.fill(BLACK)
        self.path.draw(self.screen)
        self.ball_generator.draw(self.screen)
        self.sprites.draw(self.screen)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start()
