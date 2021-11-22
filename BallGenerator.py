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
                    self.balls[-1].rect.center[0] == 2 * BALL_RADIUS:
                self.balls.append(Ball(random.choice(self.colors),
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

    def delete(self):
        pass

    def insert(self, index, shooting_ball):
        if index == 0:
            center = self.count_center(index)
            ball = Ball(shooting_ball.color, center, self.path)
        else:
            ball = Ball(shooting_ball.color, self.balls[index - 1].rect.center,
                        self.path)
        for i in range(index - 1, -1, -1):
            self.balls[i].move(8)
        self.balls.insert(index, ball)

    def destroy(self, chain):
        chain_start_index = self.balls.index(chain[0])
        chain_end_index = self.balls.index(chain[-1])

        self.remove_balls(chain)
        if chain_start_index != 0 and chain_end_index != len(self.balls) + \
                len(chain) - 1 and self.balls[chain_start_index - 1].color == \
                self.balls[chain_start_index].color:
            self.join_balls(chain_start_index - 1, chain_start_index)

    def join_balls(self, head_index, tail_index):
        color = self.balls[head_index].color
        center = self.count_center(tail_index)
        self.balls[head_index] = Ball(color, center, self.path)

    def remove_balls(self, balls):
        for ball in balls:
            self.balls.remove(ball)

    def count_center(self, index):
        return self.path.nodes[self.balls[index].pos_in_path + 2 * BALL_RADIUS
                               // self.path.step]