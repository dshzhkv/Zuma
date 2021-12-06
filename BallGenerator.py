from Params import *
from Sprites import Ball, Bonus
import random
import datetime


class BallGenerator:
    def __init__(self, path, number):
        self.path = path
        self.colors = [BLUE, RED, GREEN, YELLOW]
        self.bonuses = [Bonus.Pause]
        self.balls = []
        self.number_to_generate = number
        self.number_of_generated = 0
        self.start_time = datetime.datetime.now()

    def generate(self):
        if self.number_of_generated < self.number_to_generate:
            if len(self.balls) == 0 or \
                    self.balls[0].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.insert(0, Ball(random.choice(self.colors),
                                          self.path.nodes[0], self.path))
                self.number_of_generated += 1

    def update(self):
        for i in range(len(self.balls)):
            self.balls[i].update()

            if not self.balls[i].can_move and \
                    (i == 0 or (self.balls[i - 1].can_move and
                                self.balls[i].rect.colliderect(self.balls[i-1].rect))):
                self.balls[i].can_move = True
                # self.balls[i].rect.center = self.count_center(i - 1)
        self.generate_bonus()

    def generate_bonus(self):
        cur_time = datetime.datetime.now()
        if (cur_time - self.start_time).seconds == 15:
            ball_with_bonus = random.choice(self.balls)
            bonus = random.choice(self.bonuses)
            ball_with_bonus.set_bonus(bonus, cur_time)
            self.start_time = cur_time

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
            self.balls[i] = Ball(color, center, self.path)

    def stop_balls(self, tail_index):
        for i in range(tail_index, len(self.balls)):
            self.balls[i].can_move = False

    def count_center(self, index):
        return self.path.nodes[self.balls[index].pos_in_path + 2 * BALL_RADIUS
                               // self.path.step]

