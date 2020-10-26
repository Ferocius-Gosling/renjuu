import random
from game.player import Player


class Bot(Player):
    def make_move(self, board):
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        while board.map[x][y] != 0:
            x = random.randint(0, board.width - 1)
            y = random.randint(0, board.height - 1)
        return x, y
