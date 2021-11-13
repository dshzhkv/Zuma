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
            if len(self.balls) == 0 or \
                    self.balls[-1].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.append(Ball(random.choice(self.colors), self.path))

    def update(self):
        for ball in self.balls:
            ball.update()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def get_available_colors(self):
        return [ball.color for ball in self.balls]

    def destroy_ball(self, ball):
        ball.kill()
        self.balls.remove(ball)


class ShootingManager:
    def __init__(self, ball_generator):
        self.ball_generator = ball_generator

        self.charged_ball = ShootingBall(random.choice(
            self.ball_generator.colors))

        self.shooting_ball = None

    def shoot(self, target):
        self.shooting_ball = self.charged_ball
        self.shooting_ball.set_target(target)
        self.charged_ball = self.recharge()

    def recharge(self):
        return ShootingBall(random.choice(
            self.ball_generator.get_available_colors()))

    def draw(self, screen):
        self.charged_ball.draw(screen)
        if self.shooting_ball is not None:
            self.shooting_ball.draw(screen)

    #region update
    def update(self):
        self.charged_ball.update()
        if self.shooting_ball is not None:
            self.shooting_ball.update()
            self.handle_shoot()

    def handle_shoot(self):
        for ball in self.ball_generator.balls:
            if self.shooting_ball.rect.colliderect(ball.rect):
                self.handle_hit(ball)
                self.shooting_ball.kill()
                self.shooting_ball = None
                break

    def handle_hit(self, ball):
        if ball.color == self.shooting_ball.color:
            ball_index = self.ball_generator.balls.index(ball)
            if self.is_hit_the_chain(ball_index):
                self.destroy_chain(ball_index)

    def is_hit_the_chain(self, ball_index):
        return self.ball_generator.balls[ball_index - 1].color == \
               self.shooting_ball.color or \
               self.ball_generator.balls[ball_index + 1].color == \
               self.shooting_ball.color

    def destroy_chain(self, ball_index):
        balls_to_destroy = []
        i = ball_index - 1
        while self.ball_generator.balls[i].color == self.shooting_ball.color:
            balls_to_destroy.append(self.ball_generator.balls[i])
            i -= 1
        i = ball_index + 1
        while self.ball_generator.balls[i].color == self.shooting_ball.color:
            balls_to_destroy.append(self.ball_generator.balls[i])
            i += 1
        balls_to_destroy.append(self.ball_generator.balls[ball_index])
        for ball in balls_to_destroy:
            self.ball_generator.destroy_ball(ball)
    #endregion


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
        self.shooting_manager = ShootingManager(self.ball_generator)

    def play(self):
        isRunning = True

        while isRunning:
            self.ball_generator.generate()

            self.clock.tick(FPS)

            for event in pygame.event.get():
                isRunning = self.handle_event(event)

            self.update_sprites()
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

    def update_display(self):
        self.screen.fill(BLACK)

        self.path.draw(self.screen)

        self.ball_generator.draw(self.screen)
        self.player.draw(self.screen)
        self.shooting_manager.draw(self.screen)

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.play()
