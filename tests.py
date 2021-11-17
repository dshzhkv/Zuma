from unittest import TestCase
from Params import *
from unittest.mock import patch
from main import BallGenerator
from Path import Path
from Sprites import *


class Test_BallGenerator(TestCase):
    path = Path()

    def test_insertBallInMiddle_length_changed(self):
        ball = Ball(GREEN, SCREEN_CENTER, self.path)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, ball)
        assert len(ball_generator.balls) == 4

    def test_insertBallInMiddle_right_ball_at_right_place(self):
        shooting_ball = ShootingBall(GREEN)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, shooting_ball)

        ball_0 = ball_generator.balls[0]
        ball_1 = ball_generator.balls[1]
        ball_2 = ball_generator.balls[2]
        ball_3 = ball_generator.balls[3]

        assert (ball_1.color == shooting_ball.color and
                ball_1.rect.center == (120, 80)) is True
        assert (ball_0.color == BLUE and ball_0.rect.center == (160, 80))
        assert (ball_2.color == GREEN and ball_2.rect.center == (80, 80))
        assert (ball_3.color == YELLOW and ball_3.rect.center == (40, 80))

    def test_insertBallInHead(self):
        shooting_ball = ShootingBall(GREEN)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(0, shooting_ball)

        ball_0 = ball_generator.balls[0]
        ball_1 = ball_generator.balls[1]
        ball_2 = ball_generator.balls[2]
        ball_3 = ball_generator.balls[3]

        assert (ball_0.color == shooting_ball.color and
                ball_0.rect.center == (160, 80)) is True
        assert (ball_1.color == BLUE and
                ball_1.rect.center == (120, 80)) is True
        assert (ball_2.color == GREEN and
                ball_2.rect.center == (80, 80)) is True
        assert (ball_3.color == YELLOW and
                ball_3.rect.center == (40, 80)) is True

    def test_insert_and_move(self):
        pass

    def create_ball_generator(self):
        ball_generator = BallGenerator(self.path, 3)
        ball_generator.balls = [Ball(BLUE, (120, 80), self.path),
                                Ball(GREEN, (80, 80), self.path),
                                Ball(YELLOW, (40, 80), self.path)]
        return ball_generator
