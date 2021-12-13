from unittest import TestCase

from game.Path import Path
from game.BallGenerator import BallGenerator
from game.Sprites import *
from game.images import *
from game.ShootingManager import ShootingManager
from game.BonusManager import BonusManager, Bonus
from game.ScoreManager import ScoreManager


def are_lists_equal(expected, actual):
    if len(expected) != len(actual):
        return False

    for i in range(len(expected)):
        if expected[i] != actual[i]:
            return False

    return True


def setup_ball_generator(path, colors):
    ball_generator = BallGenerator(path, len(colors), ScoreManager())
    ball_generator.balls = setup_balls(path, colors)
    return ball_generator


def setup_balls(path, colors):
    positions = setup_positions(path, len(colors))
    return [Ball(colors[i], positions[i], path) for i in range(len(colors))]


def setup_positions(path, length):
    step = 2 * BALL_RADIUS // path.step
    return [i for i in range(0, length * step + 1, step)]


def setup_shooting_manager(ball_generator, shooting_ball_color):
    shooting_manager = ShootingManager(ball_generator, SCREEN_CENTER,
                                       BonusManager(ball_generator),
                                       ScoreManager())
    shooting_manager.shooting_balls = [ShootingBall(shooting_ball_color)]
    return shooting_manager


class TestInsert(TestCase):
    def test_insert_ball_in_middle_path1(self):
        assert self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 1,
                               [YELLOW, GREEN, RED, BLUE]) is True

    def test_insert_ball_in_head_path1(self):
        assert self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 2,
                               [YELLOW, GREEN, BLUE, RED]) is True

    def test_insert_ball_in_tail_path1(self):
        assert self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 0,
                               [YELLOW, RED, GREEN, BLUE]) is True

    def test_insert_ball_in_middle_path2(self):
        assert self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 1,
                               [YELLOW, GREEN, RED, BLUE]) is True

    def test_insert_ball_in_head_path2(self):
        assert self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 2,
                               [YELLOW, GREEN, BLUE, RED]) is True

    def test_insert_ball_in_tail_path2(self):
        assert self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 0,
                               [YELLOW, RED, GREEN, BLUE]) is True

    def test_insert_ball_in_middle_path3(self):
        assert self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 1,
                               [YELLOW, GREEN, RED, BLUE]) is True

    def test_insert_ball_in_head_path3(self):
        assert  self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 2,
                                [YELLOW, GREEN, BLUE, RED]) is True

    def test_insert_ball_in_tail_path3(self):
        assert self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 0,
                               [YELLOW, RED, GREEN, BLUE]) is True

    @staticmethod
    def setup_test(shooting_ball_color, path_num, balls_colors,
                   insert_index, expected_colors):
        shooting_ball = ShootingBall(shooting_ball_color)
        path = Path(path_num)
        ball_generator = setup_ball_generator(path, balls_colors)
        ball_generator.insert(insert_index, shooting_ball)
        balls_expected = setup_balls(path, expected_colors)
        return are_lists_equal(balls_expected, ball_generator.balls)


class TestCollectChain(TestCase):
    def test_collect_chain_from_tail(self):
        assert self.setup_test(1, [GREEN, GREEN, BLUE, BLUE], GREEN, 0,
                               [0, 1]) is True

    def test_collect_chain_from_head(self):
        assert self.setup_test(1, [GREEN, GREEN, BLUE, BLUE], BLUE, 3,
                               [2, 3]) is True

    def test_collect_chain_from_middle(self):
        assert self.setup_test(1, [GREEN, BLUE, BLUE, GREEN], BLUE, 1,
                               [1, 2]) is True

    def test_no_chain(self):
        assert self.setup_test(1, [GREEN] * 4, BLUE, 2, []) is True

    def test_collect_chain_startFromDifferentColor(self):
        assert self.setup_test(1, [BLUE, GREEN, GREEN, GREEN], GREEN, 0,
                               [1, 2, 3]) is True

    def test_collect_one_ball(self):
        assert self.setup_test(1, [BLUE, GREEN, RED, YELLOW], GREEN, 1,
                               [1]) is True

    @staticmethod
    def setup_test(level, balls_colors, shooting_ball_color, start_index,
                   expected_indexes):
        ball_generator = setup_ball_generator(Path(level), balls_colors)
        shooting_manager = setup_shooting_manager(ball_generator,
                                                  shooting_ball_color)
        chain_actual = shooting_manager.collect_chain(ball_generator.balls[
                                                          start_index],
                                                      shooting_ball_color)
        chain_expected = [ball_generator.balls[i] for i in expected_indexes]
        return are_lists_equal(chain_expected, chain_actual)


class TestDestroy(TestCase):

    def test_destroy(self):
        ball_generator = setup_ball_generator(Path(1),
                                              [GREEN, BLUE, BLUE, RED])
        balls_expected = [ball_generator.balls[0], ball_generator.balls[3]]
        ball_generator.destroy([ball_generator.balls[1],
                                ball_generator.balls[2]])
        assert are_lists_equal(balls_expected, ball_generator.balls) is True


class TestUpdateChain(TestCase):

    path = Path(1)

    def test_join_two_balls(self):
        ball_generator = self.setup_test([RED, BLUE, BLUE, RED], [1, 2])
        assert self.are_moved(ball_generator.balls) is True

    def test_join_many_balls(self):
        colors = [RED, BLUE, BLUE, RED] + [GREEN, YELLOW] * 5
        ball_generator = self.setup_test(colors, [1, 2])
        assert self.are_moved(ball_generator.balls) is True

    def test_stop_one_ball(self):
        ball_generator = self.setup_test([RED, BLUE, BLUE, GREEN], [1, 2])
        assert self.are_stopped(1, ball_generator.balls) is True

    def test_stop_many_balls(self):
        colors = [RED, BLUE, BLUE] + [GREEN, YELLOW] * 5
        ball_generator = self.setup_test(colors, [1, 2])
        assert self.are_stopped(1, ball_generator.balls) is True

    def setup_test(self, colors, destroy_indexes):
        ball_generator = setup_ball_generator(self.path, colors)
        ball_generator.destroy([ball_generator.balls[i] for i in
                                destroy_indexes])
        ball_generator.update_chain()
        return ball_generator

    def are_moved(self, balls):
        for i in range(1, len(balls)):
            if balls[i].pos_in_path - balls[i - 1].pos_in_path != 2 * \
                    BALL_RADIUS // self.path.step:
                return False
        return True

    @staticmethod
    def are_stopped(start_index, balls):
        for i in range(0, start_index):
            if not balls[i].can_move:
                return False

        for i in range(start_index, len(balls)):
            if balls[i].can_move:
                return False

        return True


class TestBonus(TestCase):

    def test_bomb(self):
        ball_generator = setup_ball_generator(Path(1), [YELLOW] * 4 +
                                              [BLUE] * 2 + [RED] * 4)

        ball_generator.balls[4].set_bonus(Bonus.Bomb)
        balls_expected = [ball_generator.balls[0], ball_generator.balls[-1]]
        shooting_manager = setup_shooting_manager(ball_generator, BLUE)
        chain = shooting_manager.collect_chain(ball_generator.balls[4], BLUE)
        chain += shooting_manager.check_for_bonus(chain)
        ball_generator.destroy(chain)

        assert are_lists_equal(balls_expected, ball_generator.balls) is True




