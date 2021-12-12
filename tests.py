from unittest import TestCase

from game.Path import Path
from game.BallGenerator import BallGenerator
from game.Sprites import *
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


class TestInsert(TestCase):
    def test_insert_ball_in_middle_path1(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 1, [YELLOW, GREEN,
                                                               RED, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_head_path1(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 2, [YELLOW, GREEN,
                                                               BLUE, RED])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_tail_path1(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 1, [YELLOW, GREEN, BLUE], 0, [YELLOW, RED,
                                                               GREEN, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_middle_path2(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 1, [YELLOW, GREEN,
                                                               RED, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_head_path2(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 2, [YELLOW, GREEN,
                                                               BLUE, RED])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_tail_path2(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 2, [YELLOW, GREEN, BLUE], 0, [YELLOW, RED,
                                                               GREEN, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_middle_path3(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 1, [YELLOW, GREEN,
                                                               RED, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_head_path3(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 2, [YELLOW, GREEN,
                                                               BLUE, RED])
        assert are_lists_equal(balls_expected, balls_actual) is True

    def test_insert_ball_in_tail_path3(self):
        balls_expected, balls_actual = \
            self.setup_test(RED, 3, [YELLOW, GREEN, BLUE], 0, [YELLOW, RED,
                                                               GREEN, BLUE])
        assert are_lists_equal(balls_expected, balls_actual) is True

    @staticmethod
    def setup_test(shooting_ball_color, path_num, balls_colors,
                   insert_index, expected_colors):
        shooting_ball = ShootingBall(shooting_ball_color)
        path = Path(path_num)
        ball_generator = setup_ball_generator(path, balls_colors)
        ball_generator.insert(insert_index, shooting_ball)
        balls_expected = setup_balls(path, expected_colors)
        return balls_expected, ball_generator.balls


#
# class TestCollectChain(TestCase):
#
#     def test_collect_chain_from_middle(self):
#         chains = self.setup_chains([GREEN, BLUE, BLUE, GREEN], BLUE, 2,
#                                    [1, 2])
#         assert are_lists_equal(chains[0], chains[1]) is True
#
#     def test_collect_chain_from_head(self):
#         chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], GREEN, 0,
#                                    [0, 1])
#         assert are_lists_equal(chains[0], chains[1]) is True
#
#     def test_collect_chain_from_tail(self):
#         chains = self.setup_chains([GREEN, GREEN, BLUE, BLUE], BLUE, 3,
#                                    [2, 3])
#         assert are_lists_equal(chains[0], chains[1]) is True
#
#     def test_collect_chain_from_tail_startDifferentColor(self):
#         chains = self.setup_chains([GREEN, BLUE, GREEN, GREEN], GREEN, 1,
#                                    [2, 3])
#         assert are_lists_equal(chains[0], chains[1]) is True
#
#     def test_chain_one_ball(self):
#         ball_generator = self.setup_ball_generator([GREEN, BLUE, RED, YELLOW])
#         shooting_manager = self.setup_shooting_manager(ball_generator,
#                                                        BLUE)
#         chain_expected = [ball_generator.balls[1]]
#         chain_actual = shooting_manager.collect_chain(1, BLUE)
#         assert are_lists_equal(chain_expected, chain_actual)
#
#     def test_no_chain(self):
#         ball_generator = self.setup_ball_generator([GREEN, GREEN, GREEN, GREEN])
#         shooting_manager = self.setup_shooting_manager(ball_generator,
#                                                        BLUE)
#         chain_expected = []
#         chain_actual = shooting_manager.collect_chain(1, BLUE)
#         assert are_lists_equal(chain_expected, chain_actual)
#
#     def setup_chains(self, balls_colors, shooting_ball_color, start_index,
#                      expected_balls_indexes):
#         ball_generator = self.setup_ball_generator(balls_colors)
#         shooting_manager = self.setup_shooting_manager(ball_generator,
#                                                        shooting_ball_color)
#         chain_expected = [ball_generator.balls[expected_balls_indexes[0]],
#                           ball_generator.balls[expected_balls_indexes[1]]]
#         chain_actual = shooting_manager.collect_chain(start_index,
#                                                       shooting_ball_color)
#         return chain_expected, chain_actual
#
#     @staticmethod
#     def setup_ball_generator(balls_colors):
#         path = Path()
#         ball_generator = BallGenerator(path, 4)
#         ball_generator.balls = [Ball(balls_colors[0], (0, 80), path),
#                                 Ball(balls_colors[1], (40, 80), path),
#                                 Ball(balls_colors[2], (80, 80), path),
#                                 Ball(balls_colors[3], (120, 80), path)]
#         return ball_generator
#
#     @staticmethod
#     def setup_shooting_manager(ball_generator, shooting_ball_color):
#         shooting_manager = ShootingManager(ball_generator)
#         shooting_manager.shooting_balls = [ShootingBall(shooting_ball_color)]
#         return shooting_manager
#
#
# class TestDestroy(TestCase):
#
#     path = Path()
#     balls_colors = [GREEN, BLUE, BLUE, RED]
#     ball_generator = BallGenerator(path, 4)
#     ball_generator.balls = [Ball(balls_colors[0], (40, 80), path),
#                             Ball(balls_colors[1], (80, 80), path),
#                             Ball(balls_colors[2], (120, 80), path),
#                             Ball(balls_colors[3], (160, 80), path)]
#     ball_generator.destroy([ball_generator.balls[1],
#                             ball_generator.balls[2]])
#
#     def test_destroy_length_changed(self):
#         assert len(self.ball_generator.balls) == 2
#
#     def test_destroy_chain_deleted(self):
#         assert (self.ball_generator.balls[0].color == GREEN and
#                 self.ball_generator.balls[-1].color == RED) is True
#
#
# class TestJoinAndStop(TestCase):
#
#     path = Path()
#
#     def test_join_two_balls(self):
#         ball_generator = self.setup_ball_generator(2)
#         ball_generator.join_balls(1)
#         assert ball_generator.balls[1].rect.pos == (40, 80)
#
#     def test_join_many_balls(self):
#         ball_generator = self.setup_ball_generator(20)
#         ball_generator.join_balls(1)
#
#         expected_balls = self.setup_balls(20, (0, 80), GREEN)
#
#         assert are_lists_equal(expected_balls, ball_generator.balls) is True
#
#     def test_stop_one_ball(self):
#         ball_generator = self.setup_ball_generator(2)
#         ball_generator.stop_balls(1)
#         expected = [True, False]
#         actual = [ball.can_move for ball in ball_generator.balls]
#
#         assert are_lists_equal(expected, actual) is True
#
#     def test_stop_many_balls(self):
#         ball_generator = self.setup_ball_generator(20)
#         ball_generator.stop_balls(1)
#
#         expected = [True] + [False] * 19
#         actual = [ball.can_move for ball in ball_generator.balls]
#
#         assert are_lists_equal(expected, actual) is True
#
#     def setup_ball_generator(self, number_of_balls):
#         ball_generator = BallGenerator(self.path, number_of_balls)
#         ball_generator.balls = [Ball(GREEN, (0, 80), self.path)]
#         ball_generator.balls += self.setup_balls(number_of_balls - 1, (80, 80),
#                                                  GREEN)
#
#         return ball_generator
#
#     def setup_balls(self, amount, start_pos, color):
#         start_pos = self.path.nodes.index(start_pos)
#         step = (2 * BALL_RADIUS // self.path.step)
#         end_pos = start_pos + step * amount
#         positions = [self.path.nodes[i] for i in range(start_pos, end_pos,
#                                                        step)]
#         return [Ball(color, pos, self.path) for pos in positions]
#
#
# class TestHit(TestCase):
#     path = Path()
#
#     def test_one_combo_hit(self):
#         ball_generator = self.setup_ball_generator([GREEN, BLUE, BLUE, GREEN,
#                                                     GREEN])
#         assert are_lists_equal([], ball_generator.balls) is True
#
#     def test_stop_after_hit(self):
#         ball_generator = self.setup_ball_generator([RED, BLUE, BLUE, GREEN,
#                                                     YELLOW])
#         ball_0 = Ball(RED, (0, 80), self.path)
#         ball_1 = Ball(GREEN, (120, 80), self.path)
#         ball_2 = Ball(YELLOW, (160, 80), self.path)
#         ball_1.can_move = ball_2.can_move = False
#         expected = [ball_0, ball_1, ball_2]
#
#         assert are_lists_equal(expected, ball_generator.balls) is True
#
#     def test_join_after_hit(self):
#         ball_generator = self.setup_ball_generator([GREEN, BLUE, BLUE, GREEN,
#                                                     YELLOW])
#         ball_0 = Ball(GREEN, (0, 80), self.path)
#         ball_1 = Ball(GREEN, (40, 80), self.path)
#         ball_2 = Ball(YELLOW, (80, 80), self.path)
#         expected = [ball_0, ball_1, ball_2]
#
#         assert are_lists_equal(expected, ball_generator.balls) is True
#
#     def test_three_combo_after_hit(self):
#         pass
#
#     def setup_ball_generator(self, colors):
#         ball_generator = BallGenerator(self.path, 5)
#
#         positions = [(i, 80) for i in range(0, 161, 40)]
#         ball_generator.balls = [Ball(colors[i], positions[i], self.path)
#                                 for i in range(5)]
#
#         shooting_manager = ShootingManager(ball_generator)
#         shooting_manager.handle_combo([ball_generator.balls[1],
#                                        ball_generator.balls[2]])
#         shooting_manager.update()
#         ball_generator.update()
#
#         return ball_generator
#
#     def test_hit_1(self):
#         ball_generator = BallGenerator(self.path, 6)
#
#         positions = [(i, 80) for i in range(0, 201, 40)]
#         colors = [RED] * 2 + [YELLOW] * 2 + [BLUE] * 2
#         ball_generator.balls = [Ball(colors[i], positions[i], self.path)
#                                 for i in range(6)]
#         shooting_manager = ShootingManager(ball_generator)
#         shooting_manager.handle_combo([ball_generator.balls[2],
#                                      ball_generator.balls[3]])
#         shooting_manager.update()
#
#         blue_ball_1 = Ball(BLUE, (160, 80), self.path)
#         blue_ball_2 = Ball(BLUE, (200, 80), self.path)
#         blue_ball_1.can_move = blue_ball_2.can_move = False
#         expected = [Ball(RED, (0, 80), self.path),
#                     Ball(RED, (40, 80), self.path), blue_ball_1, blue_ball_2]
#
#         assert are_lists_equal(expected, ball_generator.balls) is True
#
#     def test_hit_2(self):
#         ball_generator = BallGenerator(self.path, 5)
#
#         positions = [(i, 80) for i in range(0, 161, 40)]
#         colors = [BLUE] + [RED] * 2 + [BLUE] * 2
#         ball_generator.balls = [Ball(colors[i], positions[i], self.path)
#                                 for i in range(5)]
#         shooting_manager = ShootingManager(ball_generator)
#         shooting_manager.handle_combo([ball_generator.balls[1],
#                                      ball_generator.balls[2]])
#         shooting_manager.update()
#         ball_generator.update()
#
#
#         assert are_lists_equal([], ball_generator.balls) is True


# class TestBomb(TestCase):
#     def test_bomb(self):
#         path = Path(1)
#         ball_generator = BallGenerator(path, 10)
#         ball_generator.balls = [Ball(YELLOW, path.nodes[i], path) for i in range(1, 5)] + \
#                                [Ball(BLUE, path.nodes[i], path) for i in range(5, 7)] + \
#                                [Ball(RED, path.nodes[i], path) for i in range(7, 11)]
#         ball_generator.balls[4].set_bonus(Bonus.Bomb)
#         player = Player()
#         bonus_manager = BonusManager(ball_generator)
#         shooting_manager = ShootingManager(ball_generator, player, bonus_manager)
#         shooting_ball = ShootingBall(BLUE, (ball_generator.balls[4].rect.center[0], ball_generator.balls[4].rect.center[1] - 39))
#         shooting_manager.shooting_balls = [shooting_ball]
#         shooting_manager.handle_shoot(shooting_ball)
#         expected = [Ball(YELLOW, path.nodes[1], path), Ball(RED, path.nodes[10], path)]
#         assert are_lists_equal(expected, ball_generator.balls)
#
#


