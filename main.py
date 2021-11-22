import pygame
import random
import os
import math
from Params import *
from Path import Path
from Sprites import *
from BallGenerator import BallGenerator
from ShootingManager import ShootingManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Zuma")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.path = Path()
        self.ball_generator = BallGenerator(self.path, 10)
        self.finish = Finish(self.path, self.ball_generator.balls)
        self.shooting_manager = ShootingManager(self.ball_generator)

    def play(self):
        isRunning = True

        while isRunning:
            self.ball_generator.generate()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.shooting_manager.shoot(pygame.mouse.get_pos())

            self.update_sprites()
            if self.finish.isFinished or self.shooting_manager.win:
                isRunning = False
            self.update_display()

        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.shooting_manager.shoot(pygame.mouse.get_pos())
        return True

    def update_sprites(self):
        self.player.update()
        self.ball_generator.update()
        self.shooting_manager.update()
        self.finish.update()

    def update_display(self):
        self.screen.fill(BLACK)

        self.path.draw(self.screen)

        self.ball_generator.draw(self.screen)
        self.player.draw(self.screen)
        self.shooting_manager.draw(self.screen)
        self.finish.draw(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
