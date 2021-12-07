from Params import *
from Sprites import Ball, Bonus
import random
import datetime


class BallGenerator:
    def __init__(self, path, number):
        self.path = path
        self.colors = [BLUE, RED, GREEN, YELLOW]
        self.balls = []
        self.number_to_generate = number
        self.number_of_generated = 0

        self.reverse = False
        self.pause = False

    def generate(self):
        if self.number_of_generated < self.number_to_generate:
            if len(self.balls) == 0 or \
                    self.balls[0].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.insert(0, Ball(random.choice(self.colors),
                                          self.path.nodes[0], self.path))
                self.number_of_generated += 1

    def move_stopped_ball(self, i):
        if not self.balls[i].can_move:
            if i == 0:
                self.balls[i].can_move = True

            elif self.balls[i - 1].can_move and \
                    self.balls[i - 1].rect.colliderect(self.balls[i].rect):
                self.balls[i].can_move = True

    def update_balls(self):
        for i in range(len(self.balls)):
            self.balls[i].update()
            self.move_stopped_ball(i)

    def update_chain(self):
        for i in range(1, len(self.balls)):
            left_ball = self.balls[i - 1]
            right_ball = self.balls[i]
            if right_ball.pos_in_path - left_ball.pos_in_path > 20:
                if left_ball.color == right_ball.color:
                    self.join_balls(i)
                else:
                    self.stop_balls(i)

    def update(self):
        self.update_chain()
        if not self.reverse and not self.pause:
            self.update_balls()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def get_available_colors(self):
        return [ball.color for ball in self.balls]

    def insert(self, index, shooting_ball):
        if index == len(self.balls) - 1:
            center = self.count_center(index)
            ball = Ball(shooting_ball.color, center, self.path)
        else:
            ball = Ball(shooting_ball.color, self.balls[index + 1].rect.center,
                        self.path)
        ball.can_move = self.balls[index].can_move
        for i in range(index + 1, len(self.balls)):
            self.balls[i].move(2 * BALL_RADIUS // self.path.step)
        self.balls.insert(index + 1, ball)

    def destroy(self, chain):
        for ball in chain:
            self.balls.remove(ball)

    def join_balls(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            color = self.balls[i].color
            center = self.count_center(i - 1)
            # тут нужно не создавать новый мяч а просто двигат
            self.balls[i] = Ball(color, center, self.path)

    def stop_balls(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            self.balls[i].can_move = False

    def count_center(self, index):
        return self.path.nodes[self.balls[index].pos_in_path + 2 * BALL_RADIUS
                               // self.path.step]




