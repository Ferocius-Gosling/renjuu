from view.button import Button
from game.params import Color
from view.params import black_color, white_color
import pygame

pygame.init()


class Stone(Button):
    def __init__(self, width, height, board_x, board_y):
        super().__init__(width, height, black_color)
        self.board_x = board_x
        self.board_y = board_y
        self.state = Color.non

    def draw_stone(self, display, x, y, player_color):
        circle_color = black_color if \
            Color.black.value == player_color\
            else white_color
        pygame.draw.circle(display, circle_color, (x, y), 13)

