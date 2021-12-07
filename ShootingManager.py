from Sprites import ShootingBall
from Params import *
import random


class ShootingManager:
    def __init__(self, ball_generator, player, bonus_manager):
        self.ball_generator = ball_generator
        self.bonus_manager = bonus_manager
        self.player = player

        self.charged_ball = ShootingBall(random.choice(
            self.ball_generator.colors), player.pos)

        self.is_win = False

        self.shooting_balls = []

        self.combo_chain = []

        self.points = 0

    def shoot(self, target):
        shooting_ball = self.charged_ball
        shooting_ball.set_target(target)
        self.charged_ball = self.recharge()
        self.shooting_balls.append(shooting_ball)

    def recharge(self):
        return ShootingBall(random.choice(
            self.ball_generator.get_available_colors()), self.player.pos)

    def draw(self, screen):
        self.charged_ball.draw(screen)
        for ball in self.shooting_balls:
            ball.draw(screen)

    def update(self):
        self.points = 0
        self.charged_ball.update()
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
        for ball in self.ball_generator.balls:
            if shooting_ball.rect.colliderect(ball.rect):
                chain = self.ball_generator.collect_chain(ball, shooting_ball.color)
                if len(chain) > 1:
                    self.check_for_bonus(chain)
                    self.ball_generator.destroy(chain)
                    if self.charged_ball.color not in \
                            self.ball_generator.get_available_colors():
                        self.charged_ball = self.recharge()
                else:
                    ball_index = self.ball_generator.balls.index(ball)
                    self.ball_generator.insert(ball_index, shooting_ball)
                self.shooting_balls.remove(shooting_ball)
                break

    def check_for_bonus(self, chain):
        for ball in chain:
            if ball.bonus is not None:
                self.bonus_manager.start_bonus(ball.bonus)


