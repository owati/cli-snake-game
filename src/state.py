from enum import Enum

class State(Enum):
    BEGIN = 0
    PLAYING = 1
    GAME_OVER = 2
    END = 3

class SnakeDirection(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, 1)
    DOWN = (0, -1)

