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
                self.handle_hit(i, shooting_ball)
                self.shooting_balls.remove(shooting_ball)
                break

    def handle_hit(self, ball_index, shooting_ball):
        if self.is_hit_chain(ball_index, shooting_ball):
            self.ball_generator.destroy(self.collect_chain(ball_index, shooting_ball))
            if len(self.ball_generator.balls) == 0:
                self.win = True
                return
            else:
                self.recharge()
        else:
            self.ball_generator.insert(ball_index, shooting_ball)

    def is_hit_chain(self, ball_index, shooting_ball):
        if len(self.ball_generator.balls) == 1:
            return False

        if shooting_ball.color == \
                self.ball_generator.balls[ball_index].color:
            if ball_index == 0:
                if self.ball_generator.balls[ball_index + 1].color == \
                        shooting_ball.color:
                    return True
                return False

            elif ball_index == len(self.ball_generator.balls) - 1:
                if self.ball_generator.balls[ball_index - 1].color == \
                        shooting_ball.color:
                    return True
                return False

            else:
                if self.ball_generator.balls[ball_index - 1].color == \
                        shooting_ball.color or \
                        self.ball_generator.balls[ball_index + 1].color == \
                        shooting_ball.color:
                    return True
                return False

        elif ball_index + 2 < len(self.ball_generator.balls) and \
                shooting_ball.color == \
                self.ball_generator.balls[ball_index + 1].color and \
                shooting_ball.color == \
                self.ball_generator.balls[ball_index + 2].color:
            return True

        elif ball_index - 2 >= 0 and shooting_ball.color == \
                self.ball_generator.balls[ball_index - 1].color and \
                shooting_ball.color == \
                self.ball_generator.balls[ball_index - 2].color:
            return True

        return False

    def collect_chain(self, ball_index, shooting_ball):
        chain = []

        i = ball_index - 1
        while i >= 0 and \
                self.ball_generator.balls[i].color == shooting_ball.color:
            chain.append(self.ball_generator.balls[i])
            i -= 1

        i = ball_index + 1
        while i < len(self.ball_generator.balls) and \
                self.ball_generator.balls[i].color == shooting_ball.color:
            chain.append(self.ball_generator.balls[i])
            i += 1

        if self.ball_generator.balls[ball_index].color == \
                shooting_ball.color:
            chain.append(self.ball_generator.balls[ball_index])

        chain.sort(key=lambda ball: ball.pos_in_path)

        return chain
