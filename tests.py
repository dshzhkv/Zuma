from unittest import TestCase
from game.BallGenerator import BallGenerator
from game.Path import Path
from game.Sprites import *
from game.ShootingManager import ShootingManager


def are_lists_equal(expected, actual):
    if len(expected) != len(actual):
        return False

    for i in range(len(expected)):
        if expected[i] != actual[i]:
            return False

    return True


class TestInsert(TestCase):
    path = Path()

    def test_insert_ball_in_middle(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(1, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW, GREEN,
                                                    shooting_ball.color, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_head(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(2, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW, GREEN, BLUE,
                                                    shooting_ball.color])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_tail(self):
        shooting_ball = ShootingBall(RED)
        balls_actual = self.setup_ball_generator(0, shooting_ball).balls
        balls_expected = self.setup_expected_balls([YELLOW,
                                                    shooting_ball.color, GREEN,
                                                    BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

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


class TestCollectChain(TestCase):

    def test_collect_chain_from_middle(self):
        chains = self.setup_chains([GREEN, BLUE, BLUE, GREEN], BLUE, 2,
                                   [1, 2])
        assert are_lists_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_head(self):
        chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], GREEN, 0,
                                   [0, 1])
        assert are_lists_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_tail(self):
        chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], BLUE, 3,
                                   [2, 3])
        assert are_lists_equal(chains[0], chains[1]) is True

    def test_collect_chain_from_tail_startDifferentColor(self):
        chains = self.setup_chains([GREEN, BLUE, GREEN, GREEN], GREEN, 1,
                                   [2, 3])
        assert are_lists_equal(chains[0], chains[1]) is True

    def test_chain_one_ball(self):
        ball_generator = self.setup_ball_generator([GREEN, BLUE, RED, YELLOW])
        shooting_manager = self.setup_shooting_manager(ball_generator,
                                                       BLUE)
        chain_expected = [ball_generator.balls[1]]
        chain_actual = shooting_manager.collect_chain(1, BLUE)
        assert are_lists_equal(chain_expected, chain_actual)

    def test_no_chain(self):
        ball_generator = self.setup_ball_generator([GREEN, GREEN, GREEN, GREEN])
        shooting_manager = self.setup_shooting_manager(ball_generator,
                                                       BLUE)
        chain_expected = []
        chain_actual = shooting_manager.collect_chain(1, BLUE)
        assert are_lists_equal(chain_expected, chain_actual)

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


class TestJoinAndStop(TestCase):

    path = Path()

    def test_join_two_balls(self):
        ball_generator = self.setup_ball_generator(2)
        ball_generator.join_balls(1)
        assert ball_generator.balls[1].rect.center == (40, 80)

    def test_join_many_balls(self):
        ball_generator = self.setup_ball_generator(20)
        ball_generator.join_balls(1)

        expected_balls = self.setup_balls(20, (0, 80), GREEN)

        assert are_lists_equal(expected_balls, ball_generator.balls) is True

    def test_stop_one_ball(self):
        ball_generator = self.setup_ball_generator(2)
        ball_generator.stop_balls(1)
        expected = [True, False]
        actual = [ball.can_move for ball in ball_generator.balls]

        assert are_lists_equal(expected, actual) is True

    def test_stop_many_balls(self):
        ball_generator = self.setup_ball_generator(20)
        ball_generator.stop_balls(1)

        expected = [True] + [False] * 19
        actual = [ball.can_move for ball in ball_generator.balls]

        assert are_lists_equal(expected, actual) is True

    def setup_ball_generator(self, number_of_balls):
        ball_generator = BallGenerator(self.path, number_of_balls)
        ball_generator.balls = [Ball(GREEN, (0, 80), self.path)]
        ball_generator.balls += self.setup_balls(number_of_balls - 1, (80, 80),
                                                 GREEN)

        return ball_generator

    def setup_balls(self, amount, start_pos, color):
        start_pos = self.path.nodes.index(start_pos)
        step = (2 * BALL_RADIUS // self.path.step)
        end_pos = start_pos + step * amount
        positions = [self.path.nodes[i] for i in range(start_pos, end_pos,
                                                       step)]
        return [Ball(color, pos, self.path) for pos in positions]


class TestHit(TestCase):
    path = Path()

    def test_one_combo_hit(self):
        ball_generator = self.setup_ball_generator([GREEN, BLUE, BLUE, GREEN,
                                                    GREEN])
        assert are_lists_equal([], ball_generator.balls) is True

    def test_stop_after_hit(self):
        ball_generator = self.setup_ball_generator([RED, BLUE, BLUE, GREEN,
                                                    YELLOW])
        ball_0 = Ball(RED, (0, 80), self.path)
        ball_1 = Ball(GREEN, (120, 80), self.path)
        ball_2 = Ball(YELLOW, (160, 80), self.path)
        ball_1.can_move = ball_2.can_move = False
        expected = [ball_0, ball_1, ball_2]

        assert are_lists_equal(expected, ball_generator.balls) is True

    def test_join_after_hit(self):
        ball_generator = self.setup_ball_generator([GREEN, BLUE, BLUE, GREEN,
                                                    YELLOW])
        ball_0 = Ball(GREEN, (0, 80), self.path)
        ball_1 = Ball(GREEN, (40, 80), self.path)
        ball_2 = Ball(YELLOW, (80, 80), self.path)
        expected = [ball_0, ball_1, ball_2]

        assert are_lists_equal(expected, ball_generator.balls) is True

    def test_three_combo_after_hit(self):
        pass

    def setup_ball_generator(self, colors):
        ball_generator = BallGenerator(self.path, 5)

        positions = [(i, 80) for i in range(0, 161, 40)]
        ball_generator.balls = [Ball(colors[i], positions[i], self.path)
                                for i in range(5)]

        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.handle_hit([ball_generator.balls[1],
                                     ball_generator.balls[2]])

        return ball_generator

    def test_hit_1(self):
        ball_generator = BallGenerator(self.path, 6)

        positions = [(i, 80) for i in range(0, 201, 40)]
        colors = [RED] * 2 + [YELLOW] * 2 + [BLUE] * 2
        ball_generator.balls = [Ball(colors[i], positions[i], self.path)
                                for i in range(6)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.handle_hit([ball_generator.balls[2],
                                     ball_generator.balls[3]])

        blue_ball_1 = Ball(BLUE, (160, 80), self.path)
        blue_ball_2 = Ball(BLUE, (200, 80), self.path)
        blue_ball_1.can_move = blue_ball_2.can_move = False
        expected = [Ball(RED, (0, 80), self.path),
                    Ball(RED, (40, 80), self.path), blue_ball_1, blue_ball_2]

        assert are_lists_equal(expected, ball_generator.balls) is True

    def test_hit_2(self):
        ball_generator = BallGenerator(self.path, 5)

        positions = [(i, 80) for i in range(0, 161, 40)]
        colors = [BLUE] + [RED] * 2 + [BLUE] * 2
        ball_generator.balls = [Ball(colors[i], positions[i], self.path)
                                for i in range(5)]
        shooting_manager = ShootingManager(ball_generator)
        shooting_manager.handle_hit([ball_generator.balls[1],
                                     ball_generator.balls[2]])

        assert are_lists_equal([], ball_generator.balls) is True



