from enum import Enum

directions = [(1, 0), (0, 1), (1, -1), (1, 1)]


class GameMode(Enum):
    with_bot = 0
    with_human = 1


class PlayerEntity(Enum):
    human = 0
    bot = 1


class Color(Enum):
    non = 0
    black = 1
    white = 2
