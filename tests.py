from unittest import TestCase
from Params import *
from unittest.mock import patch
from BallGenerator import BallGenerator
from Path import Path
from Sprites import *
from ShootingManager import ShootingManager


class TestInsert(TestCase):
    path = Path()

    def test_insert_ball_in_middle(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(1, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW, GREEN,
                                                    shooting_ball.color, BLUE])
        assert self.are_balls_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_head(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(2, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW, GREEN, BLUE,
                                                    shooting_ball.color])
        assert self.are_balls_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_tail(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(0, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW,
                                                    shooting_ball.color, GREEN,
                                                    BLUE])
        assert self.are_balls_equal(balls_expected, balls_actual) is True

    def setup_ball_generator(self, insert_index, shooting_ball):
        ball_generator = BallGenerator(self.path, 3)
        ball_generator.balls = [Ball(YELLOW, (40, 80), self.path),
                                Ball(GREEN, (80, 80), self.path),
                                Ball(BLUE, (120, 80), self.path)]
        ball_generator.insert(insert_index, shooting_ball)
        return ball_generator

    def setup_expected_balls(self, colors):
        centers = [(i, 80) for i in range(40, 40 * len(colors) + 1, 40)]
        return [Ball(colors[i], centers[i], self.path) for i in
                range(len(colors))]

    @staticmethod
    def are_balls_equal(expected, actual):
        if len(expected) != len(actual):
            return False

        for i in range(len(expected)):
            if expected[i] != actual[i]:
                return False

        return True


class TestCollectChain(TestCase):

    def test_collect_chain_from_middle(self):
        chains = self.setup_chains([GREEN, BLUE, BLUE, GREEN], BLUE, 2,
                                   [1, 2])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_head(self):
        chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], GREEN, 0,
                                   [0, 1])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_tail(self):
        chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], BLUE, 3,
                                   [2, 3])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_tail_startDifferentColor(self):
        chains = self.setup_chains([GREEN, BLUE, GREEN, GREEN], GREEN, 1,
                                   [2, 3])
        assert self.are_chains_equal(chains[0], chains[1]) is True

    def test_chain_one_ball(self):
        ball_generator = self.setup_ball_generator([GREEN, BLUE, RED, YELLOW])
        shooting_manager = self.setup_shooting_manager(ball_generator,
                                                       BLUE)
        chain_expected = [ball_generator.balls[1]]
        chain_actual = shooting_manager.collect_chain(1, BLUE)
        assert self.are_chains_equal(chain_expected, chain_actual)

    def test_no_chain(self):
        ball_generator = self.setup_ball_generator([GREEN, GREEN, GREEN, GREEN])
        shooting_manager = self.setup_shooting_manager(ball_generator,
                                                       BLUE)
        chain_expected = []
        chain_actual = shooting_manager.collect_chain(1, BLUE)
        assert self.are_chains_equal(chain_expected, chain_actual)

    def setup_chains(self, balls_colors, shooting_ball_color, start_index,
                     expected_balls_indexes):
        ball_generator = self.setup_ball_generator(balls_colors)
        shooting_manager = self.setup_shooting_manager(ball_generator,
                                                       shooting_ball_color)
        chain_expected = [ball_generator.balls[expected_balls_indexes[0]],
                          ball_generator.balls[expected_balls_indexes[1]]]
        chain_actual = shooting_manager.collect_chain(start_index,
                                                      shooting_ball_color)
        return chain_expected, chain_actual

    @staticmethod
    def setup_ball_generator(balls_colors):
        path = Path()
        ball_generator = BallGenerator(path, 4)
        ball_generator.balls = [Ball(balls_colors[0], (0, 80), path),
                                Ball(balls_colors[1], (40, 80), path),
                                Ball(balls_colors[2], (80, 80), path),
                                Ball(balls_colors[3], (120, 80), path)]
        return ball_generator

    @staticmethod
    def setup_shooting_manager(ball_generator, shooting_ball_color):
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.shooting_balls = [ShootingBall(shooting_ball_color)]
        return shooting_manager

    @staticmethod
    def are_chains_equal(expected, actual):
        if len(expected) != len(actual):
            return False

        for i in range(len(expected)):
            if expected[i] != actual[i]:
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




