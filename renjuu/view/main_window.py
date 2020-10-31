from renjuu.game.game import Game
from renjuu.game import params as gp, const as c
from renjuu.view import params as p, button as b
from renjuu.view.click_handler import ClickHandler
from renjuu.view.utils import get_coordinates
import pygame


class MainWindow:
    def __init__(self):
        self.game = Game(gp.board_width, gp.board_height, gp.length_to_win, gp.type_of_enemy)
        self.display = pygame.display.set_mode((p.screen_width, p.screen_height))
        self.display.fill(p.menu_color)
        self.clock = pygame.time.Clock()
        self.points = []

    def open_start_menu(self):
        start_button = b.Button(100, 65, p.board_color)
        start_button.draw(self.display, p.screen_width // 2.5, p.screen_height // 2)
        self.clock.tick(15)
        launching = True
        while launching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launching = False
            pygame.display.update()

    def open_settings_menu(self):
        self.display.fill(p.menu_color)
        black_button = b.Button(120, 70, p.black_color)
        white_button = b.Button(120, 70, p.white_color)
        choice = True
        while choice:
            black_button.draw(self.display, 230, 300, action=None)
            white_button.draw(self.display, 470, 300, action=None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choice = False
            if black_button.is_pressed:
                choice = False
                self.game_on_board(c.Color.black)
            if white_button.is_pressed:
                choice = False
                self.game_on_board(c.Color.white)
            pygame.display.update()

    def game_on_board(self, color):
        self.display.blit(p.board_back, (0, 0))
        self.game.prepare_players(color)
        pygame.time.wait(200)
        click_handler = ClickHandler()
        cycle = True
        self.clock.tick(20)
        while cycle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False
            click_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            current_player = self.game.current_player
            if current_player.entity == c.PlayerEntity.human:
                if click_handler.check_click(click_pos, click):
                    if click_handler.handle() is not None:
                        x, y = click_handler.handle()
                        self.game.make_turn(x,y)
                    else:
                        continue
            else:
                x, y = current_player.make_move(self.game.board)
                self.game.make_turn(x, y)
            if self.game.winner is not None:
                pygame.time.wait(150)
                cycle = False
                self.end_game()
            self.update_map()
            pygame.display.update()

    def end_game(self):
        self.display.fill(p.board_color)
        again_button = b.Button(120, 70, p.blue_color)
        quit_button = b.Button(120, 70, p.red_color)
        game_over = True
        while game_over:
            again_button.draw(self.display, 230, 200, action=None)
            quit_button.draw(self.display, 470, 200, action=None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
            if again_button.is_pressed:
                game_over = False
                self.game.restart()
                self.open_settings_menu()
            if quit_button.is_pressed:
                game_over = False
            pygame.display.update()

    def update_map(self):
        for i in range(self.game.board.width):
            for j in range(self.game.board.height):
                if self.game.board.map[i][j] != 0:
                    self.draw_stone(self.game.board.map[i][j],
                                    get_coordinates(i, j))

    def draw_stone(self, color, pos):
        circle_color = p.black_color if \
            c.Color.black.value == color \
            else p.white_color
        pygame.draw.circle(self.display,
                           circle_color,
                           pos,
                           10)
