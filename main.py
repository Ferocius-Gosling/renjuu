import pygame
import argparse
from view import main_window
from game.const import GameMode

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--enemy', '-e', default='b', help='type of enemy player.'
                                                           ' Default(b) - bot player'
                                                           ' h - human player')
    from game import params
    namespace = parser.parse_args()
    if namespace.enemy == 'p':
        params.type_of_enemy = GameMode.with_human
    else:
        params.type_of_enemy = GameMode.with_bot
    pygame.init()

    window = main_window.MainWindow()
    window.open_settings_menu()
    pygame.quit()
