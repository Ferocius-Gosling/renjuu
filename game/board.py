from game.params import *
from game.player import Player


class Board:
    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length_to_win = length
        self.map = self.prepare_map()

    def prepare_map(self):
        points_array = []
        for i in range(self.width):
            points_array.append([])
            for j in range(self.height):
                points_array[i].append(Color.non.value)
        return points_array

    def check_around(self, x, y, color):
        directions = []
        for i in delta:
            for j in delta:
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    if self.map[x+i][y+j] == color.value:
                        directions.append((i, j))
        return directions

    def find_line(self, x, y, color, direction, second_dir):
        length = self.build_line(x, y, color, direction, 1)
        if second_dir is not None:
            length += self.build_line(x, y, color, second_dir, 0)
        if length >= self.length_to_win:
            return color
        return None

    @staticmethod
    def find_second_dir(direction, dirs):
        for second_dir in dirs:
            condition = direction[0] + second_dir[0] == 0 and \
                direction[1] + second_dir[1] == 0
            if condition:
                return second_dir
        return None

    def get_condition(self, x, y):
        condition = x < 0 or \
                y < 0 or \
                y >= self.height or \
                x >= self.width
        return condition

    def build_line(self, x, y, color, direction, length):
        dir_x = direction[0]
        dir_y = direction[1]
        while not self.get_condition(x + dir_x, y + dir_y) and\
                self.map[x + dir_x][y + dir_y] == color.value:
            length += 1
            dir_x += direction[0]
            dir_y += direction[1]
        return length
