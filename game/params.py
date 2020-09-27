from enum import Enum


board_width = 15
board_height = 15
length_to_win = 5
delta = [-1, 0, 1]


class GameStage(Enum):
    game_settings = 0
    game_on_board = 1
    end_game = 2


class Color(Enum):
    non = 0
    black = 1
    white = 2
