from Sprites import ShootingBall
import random


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

    def update(self):
        self.charged_ball.update()
        if self.shooting_ball is not None:
            self.shooting_ball.update()
            self.handle_shoot()

    def handle_shoot(self):
        for i in range(len(self.ball_generator.balls)):
            ball = self.ball_generator.balls[i]
            if self.shooting_ball.rect.colliderect(ball.rect):
                if self.is_hit_chain(i):
                    self.ball_generator.destroy(self.collect_chain(i))
                else:
                    self.ball_generator.insert(i, self.shooting_ball)
                self.shooting_ball = None
                break

    def is_hit_chain(self, ball_index):
        if len(self.ball_generator.balls) == 1:
            return False

        if self.shooting_ball.color == \
                self.ball_generator.balls[ball_index].color:
            if ball_index == 0:
                if self.ball_generator.balls[ball_index + 1].color == \
                        self.shooting_ball.color:
                    return True
                return False

            elif ball_index == len(self.ball_generator.balls) - 1:
                if self.ball_generator.balls[ball_index - 1].color == \
                        self.shooting_ball.color:
                    return True
                return False

            else:
                if self.ball_generator.balls[ball_index - 1].color == \
                        self.shooting_ball.color or \
                        self.ball_generator.balls[ball_index + 1].color == \
                        self.shooting_ball.color:
                    return True
                return False

        return False

    def collect_chain(self, ball_index):
        chain = [self.ball_generator.balls[ball_index]]
        i = ball_index - 1
        while i >= 0 and \
                self.ball_generator.balls[i].color == self.shooting_ball.color:
            chain.append(self.ball_generator.balls[i])
            i -= 1

        i = ball_index + 1
        while i < len(self.ball_generator.balls) and \
                self.ball_generator.balls[i].color == self.shooting_ball.color:
            chain.append(self.ball_generator.balls[i])
            i += 1

        chain.sort(key=lambda ball: ball.pos_in_path)

        return chain
