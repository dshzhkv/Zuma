import datetime
import random
from enum import Enum


class Bonus(Enum):
    Pause = 0
    Reverse = 1
    Bomb = 2


class BonusManager:
    def __init__(self, ball_generator):
        self.ball_generator = ball_generator
        self.bonuses = [Bonus.Pause, Bonus.Reverse, Bonus.Bomb]
        self.game_start_time = datetime.datetime.now()
        self.pause_start_time = None
        self.reverse_start_time = None
        self.explode_chain = []

        self.balls_with_bonuses = []

    def start_bonus(self, bonus):
        if bonus is Bonus.Pause:
            self.start_pause()
        elif bonus is Bonus.Reverse:
            self.start_reverse()

    def start_reverse(self):
        self.pause_start_time = datetime.datetime.now()
        self.ball_generator.reverse = True

    def start_pause(self):
        self.pause_start_time = datetime.datetime.now()
        self.ball_generator.pause = True

    def stop_reverse(self):
        self.reverse_start_time = None
        self.ball_generator.reverse = False

    def stop_pause(self):
        self.pause_start_time = None
        self.ball_generator.pause = False

    def handle_reverse_bonus(self):
        if self.reverse_start_time is not None:
            if (datetime.datetime.now() - self.reverse_start_time).seconds < 4:
                for i in range(len(self.ball_generator.balls)):
                    if self.ball_generator.balls[i].pos_in_path == 0:
                        self.reverse_start_time = None
                    else:
                        self.ball_generator.balls[i].move(-1)
            else:
                self.stop_reverse()

    def handle_pause_bonus(self):
        if self.pause_start_time is not None:
            if (datetime.datetime.now() - self.pause_start_time).seconds == 5:
                self.stop_pause()

    def update(self):
        self.handle_reverse_bonus()
        self.handle_pause_bonus()
        self.update_balls_with_bonuses()
        self.generate_bonus()

    def generate_bonus(self):
        cur_time = datetime.datetime.now()
        if (cur_time - self.game_start_time).seconds == 15:
            ball_with_bonus = random.choice(self.ball_generator.balls)
            bonus = random.choice(self.bonuses)
            ball_with_bonus.set_bonus(bonus)
            self.balls_with_bonuses.append((ball_with_bonus, cur_time))
            self.game_start_time = cur_time

    def update_balls_with_bonuses(self):
        for ball, time in self.balls_with_bonuses:
            if (datetime.datetime.now() - time).seconds == 15:
                ball.set_bonus(None)
