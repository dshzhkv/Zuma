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
        shooting_ball = ShootingBall(RED)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, shooting_ball)
        assert len(ball_generator.balls) == 4

    def test_insertBallInMiddle(self):
        shooting_ball = ShootingBall(RED)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(1, shooting_ball)

        assert self.are_balls_correct(ball_generator,
                                      [YELLOW, GREEN, shooting_ball.color,
                                       BLUE]) is True

    def test_insertBallInHead(self):
        shooting_ball = ShootingBall(RED)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(2, shooting_ball)

        assert self.are_balls_correct(ball_generator,
                                      [YELLOW, GREEN,
                                       BLUE, shooting_ball.color]) is True

    def test_insertBallInTail(self):
        shooting_ball = ShootingBall(RED)
        ball_generator = self.create_ball_generator()
        ball_generator.insert(0, shooting_ball)
        assert self.are_balls_correct(ball_generator,
                                      [YELLOW, shooting_ball.color, GREEN,
                                       BLUE]) is True

    def create_ball_generator(self):
        ball_generator = BallGenerator(self.path, 3)
        ball_generator.balls = [Ball(YELLOW, (40, 80), self.path),
                                Ball(GREEN, (80, 80), self.path),
                                Ball(BLUE, (120, 80), self.path)]
        return ball_generator

    @staticmethod
    def are_balls_correct(ball_generator, colors):
        ball0 = ball_generator.balls[0]
        ball1 = ball_generator.balls[1]
        ball2 = ball_generator.balls[2]
        ball3 = ball_generator.balls[3]

        return (ball0.color == colors[0] and ball0.rect.center == (40, 80)) \
            and (ball1.color == colors[1] and ball1.rect.center == (80, 80)) \
            and (ball2.color == colors[2] and ball2.rect.center == (120, 80)) \
            and (ball3.color == colors[3] and ball3.rect.center == (160, 80))


class TestHitChain(TestCase):

    def test_hit_chain_in_middle_true(self):
        shooting_ball_color = BLUE
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, GREEN],
                                                        shooting_ball_color)

        assert shooting_manager.is_hit_chain(1, shooting_ball_color) is True

    def test_hit_chain_in_middle_false(self):
        shooting_ball_color = GREEN
        shooting_manager = self.set_up_shooting_manager(
            [BLUE, BLUE, GREEN],
            shooting_ball_color)
        assert shooting_manager.is_hit_chain(1, shooting_ball_color) is False

    def test_hit_chain_in_head_true(self):
        shooting_ball_color = BLUE
        shooting_manager = self.set_up_shooting_manager([GREEN, BLUE, BLUE],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(2, shooting_ball_color) is True

    def test_hit_chain_in_head_false(self):
        shooting_ball_color = GREEN
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, GREEN],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(2, shooting_ball_color) is False

    def test_hit_chain_in_tail_true(self):
        shooting_ball_color = BLUE
        shooting_manager = self.set_up_shooting_manager([BLUE, BLUE, BLUE],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(0, shooting_ball_color) is True

    def test_hit_chain_it_tail_false(self):
        shooting_ball_color = GREEN
        shooting_manager = self.set_up_shooting_manager([GREEN, BLUE, BLUE],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(0, shooting_ball_color) is False

    def test_shoot_in_last_ball_false(self):
        path = Path()
        ball_generator = BallGenerator(path, 1)
        ball_generator.balls = [Ball(BLUE, (40, 80), path)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_ball_color = BLUE
        shooting_manager.shooting_ball = [ShootingBall(shooting_ball_color)]
        assert shooting_manager.is_hit_chain(0, shooting_ball_color) is False

    def test_hit_start_of_chain_true(self):
        shooting_ball_color = GREEN
        shooting_manager = self.set_up_shooting_manager([RED, GREEN, GREEN],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(0, shooting_ball_color) is True

    def test_hit_end_of_chain_true(self):
        shooting_ball_color = GREEN
        shooting_manager = self.set_up_shooting_manager([GREEN, GREEN, RED],
                                                        shooting_ball_color)
        assert shooting_manager.is_hit_chain(2, shooting_ball_color) is True

    @staticmethod
    def set_up_shooting_manager(balls_colors, shooting_ball_color):
        path = Path()
        ball_generator = BallGenerator(path, 3)
        ball_generator.balls = [Ball(balls_colors[0], (40, 80), path),
                                Ball(balls_colors[1], (80, 80), path),
                                Ball(balls_colors[2], (120, 80), path)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.shooting_balls = [ShootingBall(shooting_ball_color)]
        return shooting_manager


class TestCollectChain(TestCase):

    def test_collect_chain_from_middle(self):
        chains = self.collect_chains([GREEN, BLUE, BLUE, GREEN], BLUE, 2,
                                     [1, 2])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_head(self):
        chains = self.collect_chains([GREEN, GREEN, BLUE, BLUE], GREEN, 0,
                                     [0, 1])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_tail(self):
        chains = self.collect_chains([GREEN, GREEN, BLUE, BLUE], BLUE, 3,
                                     [2, 3])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def collect_chains(self, balls_colors, shooting_ball_color, start_index,
                       expected_balls_indexes):
        ball_generator = self.set_up_ball_generator(balls_colors)
        shooting_manager = self.set_up_shooting_manager(ball_generator,
                                                        shooting_ball_color)
        chain_expected = [ball_generator.balls[expected_balls_indexes[0]],
                          ball_generator.balls[expected_balls_indexes[1]]]
        chain_actual = shooting_manager.collect_chain(start_index,
                                                      shooting_ball_color)
        return chain_expected, chain_actual

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
        shooting_manager.shooting_balls = [ShootingBall(shooting_ball_color)]
        return shooting_manager

    @staticmethod
    def are_chains_equal(chain_1, chain_2):
        for ball in chain_1:
            if ball not in chain_2:
                return False
        return True


class TestDestroy(TestCase):

    path = Path()
    balls_colors = [GREEN, BLUE, BLUE, RED]
    ball_generator = BallGenerator(path, 4)
    ball_generator.balls = [Ball(balls_colors[0], (40, 80), path),
                            Ball(balls_colors[1], (80, 80), path),
                            Ball(balls_colors[2], (120, 80), path),
                            Ball(balls_colors[3], (160, 80), path)]
    ball_generator.destroy([ball_generator.balls[1],
                            ball_generator.balls[2]])

    def test_destroy_length_changed(self):
        assert len(self.ball_generator.balls) == 2

    def test_destroy_chain_deleted(self):
        assert (self.ball_generator.balls[0].color == GREEN and
                self.ball_generator.balls[-1].color == RED) is True

    # def test_JoinBallsAfterDestroyChain_IfSameColor(self):
    #     ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, GREEN])
    #     ball_generator.destroy(
    #         [ball_generator.balls[1], ball_generator.balls[2]])
    #     assert ball_generator.balls[1].rect.center == (80, 80)
    #
    # def test_NotJoinBallsAfterDestroyChain_IfDifferentColor(self):
    #     ball_generator = self.set_up_ball_generator([GREEN, BLUE, BLUE, RED])
    #     ball_generator.destroy(
    #         [ball_generator.balls[1], ball_generator.balls[2]])
    #     assert (ball_generator.balls[0].rect.center == (40, 80) and
    #             ball_generator.balls[1].rect.center == (160, 80)) is True
    #
    # def test_ChainInTail_ballsNotMoved(self):
    #     ball_generator = self.set_up_ball_generator([BLUE, BLUE, GREEN, RED])
    #     ball_generator.destroy(
    #         [ball_generator.balls[0], ball_generator.balls[1]])
    #     assert (ball_generator.balls[0].rect.center == (120, 80) and
    #             ball_generator.balls[1].rect.center == (160, 80)) is True
    #
    # def test_ChainInHead_ballsNotMoved(self):
    #     ball_generator = self.set_up_ball_generator([GREEN, RED, BLUE, BLUE])
    #     ball_generator.destroy(
    #         [ball_generator.balls[2], ball_generator.balls[3]])
    #     assert (ball_generator.balls[0].rect.center == (40, 80) and
    #             ball_generator.balls[1].rect.center == (80, 80)) is True




