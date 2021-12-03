import pygame
import random
import os
import math
from Params import *
from Path import Path
from Sprites import *
from BallGenerator import BallGenerator
from ShootingManager import ShootingManager
from ui import *


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
        self.finish = Finish(self.path, self.ball_generator.balls)
        self.shooting_manager = ShootingManager(self.ball_generator)
        self.ui_manager = UiManager(self.screen, self.path, self.ball_generator, self.player, self.shooting_manager, self.finish)

        self.is_quit = False

    def play(self):
        self.start_game()
        self.play_game()

        pygame.quit()

    def start_game(self):
        game_started = False

        while not game_started and not self.is_quit:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui_manager.start_game_btn.rect.collidepoint(mouse):
                        game_started = True
            self.update_display(self.ui_manager.start_window)

    def play_game(self):
        game_finished = False

        while not game_finished and not self.is_quit:
            self.ball_generator.generate()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.shooting_manager.shoot(pygame.mouse.get_pos())

            self.update_sprites()
            if self.finish.is_finished or self.shooting_manager.is_win:
                game_finished = True
            self.update_display(self.ui_manager.game_window)

    def win_game(self):
        pass

    def lose_game(self):
        pass

    def quit_game(self):
        pass

    def update_sprites(self):
        self.player.update()
        self.shooting_manager.update()
        self.ball_generator.update()
        self.finish.update()

    def update_display(self, window):
        self.ui_manager.draw_window(window)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
