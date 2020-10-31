import random
from renjuu.game.const import Color
from renjuu.game.player import Player


class Bot(Player):
    def make_move(self, board):
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        while board.map[x][y] != Color.non:
            x = random.randint(0, board.width - 1)
            y = random.randint(0, board.height - 1)
        return x, y
