from Params import *
from Sprites import Ball
import random


class BallGenerator:
    def __init__(self, path, number):
        self.path = path
        self.colors = [BLUE, RED, GREEN, YELLOW]
        self.balls = []
        self.number_to_generate = number
        self.number_of_generated = 0

    def generate(self):
        if self.number_of_generated < self.number_to_generate:
            if len(self.balls) == 0 or \
                    self.balls[0].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.insert(0, Ball(random.choice(self.colors),
                                          self.path.start, self.path))
                self.number_of_generated += 1

    def update(self):
        for ball in self.balls:
            ball.update()

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
        for i in range(index + 1, len(self.balls)):
            self.balls[i].move(2 * BALL_RADIUS // self.path.step)
        self.balls.insert(index + 1, ball)

    def destroy(self, chain):
        chain_tail = self.balls.index(chain[0])
        chain_head = self.balls.index(chain[-1])

        self.remove_balls(chain)

        if self.is_chain(chain_tail, chain_head):
            self.join_balls(chain_tail - 1)

    def is_chain(self, chain_tail, chain_head):
        if len(self.balls) == 1 or chain_tail == 0 or chain_head == \
                len(self.balls) + chain_head - chain_tail:
            return False

        if self.balls[chain_tail - 1].color == self.balls[chain_tail].color:
            return True

        return False

    def join_balls(self, tail_index):
        for i in range(tail_index + 1, len(self.balls)):
            color = self.balls[i].color
            center = self.count_center(i - 1)
            self.balls[i] = Ball(color, center, self.path)

    def remove_balls(self, balls):
        for ball in balls:
            self.balls.remove(ball)

    def count_center(self, index):
        return self.path.nodes[self.balls[index].pos_in_path + 2 * BALL_RADIUS
                               // self.path.step]
