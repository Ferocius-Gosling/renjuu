import pygame
import os

pygame.init()

screen_width = 800
screen_height = 600

board_back = pygame.image.load(os.path.join('resources', 'board.png'))
menu_color = (217, 216, 215)
black_color = (0,0,0)
red_color = (255, 0, 0)
blue_color = (0, 0, 255)
white_color = (255,255,255)
board_color = (255, 229, 180) # (209, 105, 0)

