import pygame
from renjuu.game.const import Color
import os


screen_width = 800
screen_height = 600

board_back = pygame.image.load(os.path.join('resources', 'board.png'))
menu_color = (217, 216, 215)
black_color = (0,0,0)
red_color = (255, 0, 0)
blue_color = (0, 0, 255)
green_color = (0, 255, 0)
yellow_color = (255, 255, 0)
pink_color = (255, 0, 255)
gray_color = (128, 128, 128)
white_color = (255,255,255)
board_color = (255, 229, 180) # (209, 105, 0)

check_color = {Color.black: black_color, Color.white: white_color,
               Color.red: red_color, Color.blue: blue_color,
               Color.green: green_color, Color.yellow: yellow_color,
               Color.pink: pink_color, Color.gray: gray_color}

colors = [black_color, white_color, red_color, blue_color,
          yellow_color, green_color, pink_color, gray_color]

