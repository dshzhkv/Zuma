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
                self.ball_generator.insert(i, self.shooting_ball)
                self.shooting_ball = None
                break
