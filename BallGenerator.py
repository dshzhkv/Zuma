from Params import *
from Sprites import Ball
import random


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
                self.balls.append(Ball(random.choice(self.colors),
                                       self.path.start, self.path))

    def update(self):
        for ball in self.balls:
            ball.update()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def get_available_colors(self):
        return [ball.color for ball in self.balls]

    def delete(self):
        pass

    def insert(self, index, shooting_ball):
        if index == 0:
            center = self.path.nodes[self.balls[index].pos_in_path +
                                     2 * BALL_RADIUS // self.path.step]
            ball = Ball(shooting_ball.color, center, self.path)
        else:
            ball = Ball(shooting_ball.color, self.balls[index - 1].rect.center,
                        self.path)
        for i in range(index - 1, -1, -1):
            self.balls[i].move(8)
        self.balls.insert(index, ball)
