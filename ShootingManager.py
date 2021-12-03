from Sprites import ShootingBall
from Params import *
import random


class ShootingManager:
    def __init__(self, ball_generator):
        self.ball_generator = ball_generator

        self.charged_ball = ShootingBall(random.choice(
            self.ball_generator.colors))

        self.win = False

        self.shooting_balls = []

        self.combo_chain = []

    def shoot(self, target):
        shooting_ball = self.charged_ball
        shooting_ball.set_target(target)
        self.charged_ball = self.recharge()
        self.shooting_balls.append(shooting_ball)

    def recharge(self):
        return ShootingBall(random.choice(
            self.ball_generator.get_available_colors()))

    def draw(self, screen):
        self.charged_ball.draw(screen)
        for ball in self.shooting_balls:
            ball.draw(screen)

    def update(self):
        self.charged_ball.update()
        if self.combo_chain:
            self.handle_combo(self.combo_chain)
        for ball in self.shooting_balls:
            ball.update()
            self.remove_flown_away(ball)
            self.handle_shoot(ball)

    def remove_flown_away(self, ball):
        x = ball.rect.center[0]
        y = ball.rect.center[1]
        if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            self.shooting_balls.remove(ball)

    def handle_shoot(self, shooting_ball):
        for i in range(len(self.ball_generator.balls)):
            ball = self.ball_generator.balls[i]
            if shooting_ball.rect.colliderect(ball.rect):
                chain = self.collect_chain(i, shooting_ball.color)
                if len(chain) > 1:
                    self.handle_combo(chain)
                else:
                    self.ball_generator.insert(i, shooting_ball)
                self.shooting_balls.remove(shooting_ball)
                if len(self.ball_generator.balls) == 0:
                    self.win = True
                break

    def handle_combo(self, chain):

        chain_tail = self.ball_generator.balls.index(chain[0])
        chain_head = self.ball_generator.balls.index(chain[-1])

        self.ball_generator.destroy(chain)

        if chain_tail == 0 or chain_head == len(self.ball_generator.balls) + \
                chain_head - chain_tail or \
                self.ball_generator.balls[chain_tail - 1].color != \
                self.ball_generator.balls[chain_tail].color:
            chain = []
        else:
            chain = self.collect_chain(chain_tail - 1, self.ball_generator.balls[chain_tail - 1].color)

        if len(chain) > 1:
            self.ball_generator.join_balls(chain_tail)
            chain = self.ball_generator.balls[chain_tail - 1:len(chain)]
            if len(chain) > 2:
                self.combo_chain = chain
            else:
                self.combo_chain = []
        else:
            self.combo_chain = []
            self.ball_generator.stop_balls(chain_tail)

    def collect_chain(self, ball_index, color):
        left_half = self.collect_half_chain(ball_index - 1, -1, color)
        right_half = self.collect_half_chain(ball_index + 1, 1, color)

        if self.ball_generator.balls[ball_index].color == color:
            chain = left_half + [self.ball_generator.balls[ball_index]] + \
                    right_half
            chain.sort(key=lambda ball: ball.pos_in_path)

            return chain

        if len(left_half) > len(right_half):
            return left_half
        return right_half

    def collect_half_chain(self, i, delta, color):
        half_chain = []
        while len(self.ball_generator.balls) > i >= 0 and \
                self.ball_generator.balls[i].color == color:
            half_chain.append(self.ball_generator.balls[i])
            i += delta

        return half_chain


