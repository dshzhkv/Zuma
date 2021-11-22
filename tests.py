from unittest import TestCase
from Params import *
from unittest.mock import patch
from BallGenerator import BallGenerator
from Path import Path
from Sprites import *
from ShootingManager import ShootingManager


class TestInsert(TestCase):
    path = Path()

    def test_insertBallInMiddle_length_changed(self):
        shooting_ball = ShootingBall(GREEN)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, shooting_ball)
        assert len(ball_generator.balls) == 4

    def test_insertBallInMiddle(self):
        shooting_ball = ShootingBall(GREEN)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, shooting_ball)

        assert self.are_balls_correct(ball_generator,
                                      [BLUE, shooting_ball.color,
                                       GREEN, YELLOW]) is True

    def test_insertBallInHead(self):
        shooting_ball = ShootingBall(GREEN)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(0, shooting_ball)

        assert self.are_balls_correct(ball_generator,
                                      [shooting_ball.color, BLUE,
                                       GREEN, YELLOW]) is True

    def create_ball_generator(self):
        ball_generator = BallGenerator(self.path, 3)
        ball_generator.balls = [Ball(BLUE, (120, 80), self.path),
                                Ball(GREEN, (80, 80), self.path),
                                Ball(YELLOW, (40, 80), self.path)]
        return ball_generator

    @staticmethod
    def are_balls_correct(ball_generator, colors):
        ball0 = ball_generator.balls[0]
        ball1 = ball_generator.balls[1]
        ball2 = ball_generator.balls[2]
        ball3 = ball_generator.balls[3]

        return (ball0.color == colors[0] and ball0.rect.center == (160, 80)) \
            and (ball1.color == colors[1] and ball1.rect.center == (120, 80)) \
            and (ball2.color == colors[2] and ball2.rect.center == (80, 80)) \
            and (ball3.color == colors[3] and ball3.rect.center == (40, 80))


class TestHitChain(TestCase):

    def test_hit_chain_in_middle_true(self):
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, GREEN],
                                                        BLUE)
        assert shooting_manager.is_hit_chain(1) is True

    def test_hit_chain_in_middle_false(self):
        shooting_manager = self.set_up_shooting_manager(
            [BLUE, BLUE, GREEN],
            GREEN)
        assert shooting_manager.is_hit_chain(1) is False

    def test_hit_chain_in_head_true(self):
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, GREEN],
                                                        BLUE)
        assert shooting_manager.is_hit_chain(0) is True

    def test_hit_chain_in_head_false(self):
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, GREEN],
                                                        GREEN)
        assert shooting_manager.is_hit_chain(0) is False

    def test_hit_chain_in_tail_true(self):
        shooting_manager = self.set_up_shooting_manager([GREEN, BLUE, BLUE],
                                                        BLUE)
        assert shooting_manager.is_hit_chain(2) is True

    def test_hit_chain_it_tail_false(self):
        shooting_manager = self.set_up_shooting_manager([GREEN, BLUE, BLUE],
                                                        GREEN)
        assert shooting_manager.is_hit_chain(2) is False

    def test_shoot_in_last_ball_false(self):
        path = Path()
        ball_generator = BallGenerator(path, 1)
        ball_generator.balls = [Ball(BLUE, (40, 80), path)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.shooting_ball = ShootingBall(BLUE)
        assert shooting_manager.is_hit_chain(0) is False

    @staticmethod
    def set_up_shooting_manager(balls_colors, shooting_ball_color):
        path = Path()
        ball_generator = BallGenerator(path, 3)
        ball_generator.balls = [Ball(balls_colors[0], (120, 80), path),
                                Ball(balls_colors[1], (80, 80), path),
                                Ball(balls_colors[2], (40, 80), path)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.shooting_ball = ShootingBall(shooting_ball_color)
        return shooting_manager


class TestCollectChain(TestCase):

    def test_collect_chain_from_middle(self):
        ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, GREEN])
        shooting_manager = self.set_up_shooting_manager(ball_generator, BLUE)
        chain_expected = [ball_generator.balls[1], ball_generator.balls[2]]
        chain_actual = shooting_manager.collect_chain(2)
        assert self.are_chains_equal(chain_expected, chain_actual) is True

    def test_collect_chain_from_head(self):
        ball_generator = self.set_up_ball_generator([GREEN, GREEN, BLUE, BLUE])
        shooting_manager = self.set_up_shooting_manager(ball_generator, GREEN)
        chain_expected = [ball_generator.balls[0], ball_generator.balls[1]]
        chain_actual = shooting_manager.collect_chain(0)
        assert self.are_chains_equal(chain_expected, chain_actual) is True

    def test_collect_chain_from_tail(self):
        ball_generator = self.set_up_ball_generator([GREEN, GREEN, BLUE, BLUE])
        shooting_manager = self.set_up_shooting_manager(ball_generator, BLUE)
        chain_expected = [ball_generator.balls[2], ball_generator.balls[3]]
        chain_actual = shooting_manager.collect_chain(3)
        assert self.are_chains_equal(chain_expected, chain_actual) is True

    @staticmethod
    def set_up_ball_generator(balls_colors):
        path = Path()
        ball_generator = BallGenerator(path, 4)
        ball_generator.balls = [Ball(balls_colors[0], (120, 80), path),
                                Ball(balls_colors[1], (80, 80), path),
                                Ball(balls_colors[2], (40, 80), path),
                                Ball(balls_colors[3], (0, 80), path)]
        return ball_generator

    @staticmethod
    def set_up_shooting_manager(ball_generator, shooting_ball_color):
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.shooting_ball = ShootingBall(shooting_ball_color)
        return shooting_manager

    @staticmethod
    def are_chains_equal(chain_1, chain_2):
        for ball in chain_1:
            if ball not in chain_2:
                return False
        return True


class TestDestroy(TestCase):

    def test_destroy_length_changed(self):
        ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, RED])
        ball_generator.destroy([ball_generator.balls[1], ball_generator.balls[2]])
        assert len(ball_generator.balls) == 2

    def test_destroy_chain_deleted(self):
        ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, RED])
        ball_generator.destroy([ball_generator.balls[1], ball_generator.balls[2]])
        assert (ball_generator.balls[0].color == GREEN and
                ball_generator.balls[-1].color == RED) is True

    def test_one_color_balls_moved(self):
        ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, GREEN])
        ball_generator.destroy(
            [ball_generator.balls[1], ball_generator.balls[2]])
        assert ball_generator.balls[0].rect.center == (40, 80)

    @staticmethod
    def set_up_ball_generator(balls_colors):
        path = Path()
        ball_generator = BallGenerator(path, 4)
        ball_generator.balls = [Ball(balls_colors[0], (120, 80), path),
                                Ball(balls_colors[1], (80, 80), path),
                                Ball(balls_colors[2], (40, 80), path),
                                Ball(balls_colors[3], (0, 80), path)]
        return ball_generator

