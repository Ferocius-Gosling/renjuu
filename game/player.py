from game.point import Point


class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board, x, y):
        board.map[x][y] = self.color.value
