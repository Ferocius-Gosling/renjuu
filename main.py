import pygame
# from game import params as p
from view import main_window

pygame.init()

window = main_window.MainWindow()
window.open_settings_menu()
pygame.quit()


'''
#fps check
clock = pygame.time.Clock()

#images
black_stone_image = pygame.image.load('')
white_stone_image = pygame.image.load('')
board_image = pygame.image.load('')
#нужно ещё добавить координаты гобана, но он должен быть в бекграунде.


#цикл игры, его потом запулить в game.py
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill(p.board_color)
    pygame.display.update()
    clock.tick(30)


pygame.quit()
'''