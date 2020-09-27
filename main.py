import pygame
from view import main_window

pygame.init()

window = main_window.MainWindow()
window.open_settings_menu()
pygame.quit()
