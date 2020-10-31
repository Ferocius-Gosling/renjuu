from renjuu.game.const import Color


class Board:
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length_to_win = length
        self.map = self.prepare_map()

    def __getitem__(self, item):
        return self.map[item.x][item.y]

    def __setitem__(self, key, value):
        self.map[key.x][key.y] = value

    def prepare_map(self):
        return [[Color.non] * self.height for i in range(self.width)]

    def put_stone(self, v, color):
        self[v] = color

    def get_condition(self, v):
        condition = v.x < 0 or \
                v.y < 0 or \
                v.y >= self.height or \
                v.x >= self.width
        return condition

    def find_line(self, v, direction, color, length):
        dir_first = direction
        dir_second = -direction
        while not self.get_condition(v + dir_first) and \
                self[v + dir_first] == color:
            length, dir_first = self._increment_coordinates(
                length, dir_first, direction)
        while not self.get_condition(v + dir_second) and \
                self[v + dir_second] == color:
            length, dir_second = self._increment_coordinates(
                length, dir_second, -direction)
        return length

    @staticmethod
    def _increment_coordinates(length, v, direction):
        length += 1
        v += direction
        return length, v
