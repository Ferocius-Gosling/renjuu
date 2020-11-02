from enum import Enum
from renjuu.game.vector import Vector


directions = [Vector([1, 0]), Vector([0, 1]),
              Vector([1, -1]), Vector([1, 1])]



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
    red = 3
    blue = 4
    yellow = 5
    green = 6
    pink = 7
    gray = 8

    def __lt__(self, other):
        return self.value < other.value
