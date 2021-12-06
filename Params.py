import pygame
from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (229, 44, 47)
    GREEN = (69, 153, 67)
    BLUE = (45, 80, 225)
    YELLOW = (255, 221, 58)
    TAUPE = (180, 165, 145)
    DARK_TAUPE = (173, 157, 136)
    GREY = (116, 116, 124)
    BROWN = (68, 58, 46)

WIDTH = 800
HEIGHT = 660
SCREEN_CENTER = (WIDTH / 2, HEIGHT / 2)
FPS = 30

PLAYER_SIZE = (100, 100)
BALL_SIZE = (40, 40)
BALL_RADIUS = 20

BTN_WIDTH, BTN_HEIGHT = 210, 60

FONT_SIZE = 15
