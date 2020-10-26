from game.const import Color


class Board:
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length_to_win = length
        self.map = self.prepare_map()

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value

    def prepare_map(self):
        return [[Color.non.value] * self.height for i in range(self.width)]

    def put_stone(self, x, y, color):
        self[x][y] = color.value

    def get_condition(self, x, y):
        condition = x < 0 or \
                y < 0 or \
                y >= self.height or \
                x >= self.width
        return condition

    def find_line(self, x, y, direction, color, length):
        dir_x_first = direction[0]
        dir_y_first = direction[1]
        dir_x_second = -direction[0]
        dir_y_second = -direction[1]
        inverse_dir = (-direction[0],-direction[1])
        while not self.get_condition(x + dir_x_first, y + dir_y_first) and \
                self[x + dir_x_first][y + dir_y_first] == color.value:
            length, dir_x_first, dir_y_first = self._increment_coordinates(
                length, dir_x_first, dir_y_first, direction)
        while not self.get_condition(x + dir_x_second, y + dir_y_second) and \
                self[x + dir_x_second][y + dir_y_second] == color.value:
            length, dir_x_second, dir_y_second = self._increment_coordinates(
                length, dir_x_second, dir_y_second, inverse_dir)
        return length

    @staticmethod
    def _increment_coordinates(length, x, y, direction):
        length += 1
        x += direction[0]
        y += direction[1]
        return length, x, y
