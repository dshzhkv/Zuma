from unittest import TestCase
from main import BallGenerator
from Path import Path


class Test_BallGenerator(TestCase):
    def __init__(self):
        super().__init__()
        self.path = Path()
        self.ball_generator = BallGenerator(self.path, 5)
        for _ in range(5):
            self.ball_generator.generate()
            self.ball_generator.update()

    def test_balls_moved(self):
        assert self.ball_generator.balls[-1].rect.center == (160, 80)
