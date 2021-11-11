import pygame
import random
import os
import math
from Params import *
from Turtle import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        turtle = Turtle()
        self.sprites = pygame.sprite.Group(turtle)

    def start(self):
        isRunning = True

        while isRunning:

            self.clock.tick(FPS)

            for event in pygame.event.get():
                isRunning = self.handle_event(event)

            self.sprites.update()
            self.update_display()

        pygame.quit()

    @staticmethod
    def handle_event(event):
        if event.type == pygame.QUIT:
            return False
        return True

    def update_display(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start()
