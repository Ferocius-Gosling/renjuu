import random


class Bot:
    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        while board.map[x][y] != 0:
            x = random.randint(0, board.width - 1)
            y = random.randint(0, board.height - 1)
        board.map[x][y] = self.color.value
        return x, y
