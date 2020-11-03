from renjuu.game.game import Game
from renjuu.game import params as gp, const as c
from renjuu.game.player import HumanPlayer
from renjuu.game.bot_player import Bot
from renjuu.game.vector import Vector
from renjuu.view import params as p, button as b
from renjuu.view.click_handler import ClickHandler
from renjuu.view.utils import get_coordinates, info_inc, info_dec
import pygame


class MainWindow:
    def __init__(self):
        self.game = None
        self.display = pygame.display.set_mode((p.screen_width, p.screen_height))
        self.display.fill(p.menu_color)
        self.clock = pygame.time.Clock()

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
        buttons = []
        start_button = b.Button(120, 70, p.black_color)
        player_counter_button = b.Button(120, 70, p.menu_color, info="2")
        inc_button = b.Button(50, 70, p.white_color)
        dec_button = b.Button(50, 70, p.white_color)
        switches = []
        i = 1
        for color in p.colors:
            buttons.append(b.SwitchButton(50, 50, [color, p.menu_color],
                                          [None, None], [c.Color(i), c.Color(i)]))
            i += 1
        for i in range(8):
            switches.append(b.SwitchButton(100, 50,
                                           [p.menu_color, p.menu_color],
                                           ["Human", "Bot"],
                                           [HumanPlayer(buttons[i].current_item),
                                            Bot(buttons[i].current_item,
                                                c.PlayerEntity.bot)]))
        choice = True
        while choice:
            self.draw_button(75, 50, player_counter_button, buttons)
            self.draw_button(140, 50, player_counter_button, switches)
            player_counter_button.draw(self.display, 300, 100)
            inc_button.draw(self.display, 240, 100, player_counter_button, action=info_inc)
            dec_button.draw(self.display, 400, 100, player_counter_button, action=info_dec)
            start_button.draw(self.display, 570, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choice = False
            if start_button.is_pressed:
                choice = False
                self.game_on_board(self.collect_players(int(player_counter_button.info), switches))
            pygame.display.update()

    def game_on_board(self, players):
        self.game = Game(gp.board_width, gp.board_height, gp.length_to_win, players)
        self.display.blit(p.board_back, (0, 0))
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
                        self.game.make_turn(Vector([x, y]))
                    else:
                        continue
            else:
                x, y = current_player.make_move(self.game.board)
                self.game.make_turn(Vector([x, y]))
            if pygame.key.get_pressed()[pygame.K_z]:
                self.game.undo_turn()
                pygame.time.wait(150)
                self.clear()
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
                if self.game.board.map[i][j] != c.Color.non:
                    self.draw_stone(self.game.board.map[i][j],
                                    get_coordinates(i, j))

    def clear(self):
        self.display.blit(p.board_back, (0, 0))

    def draw_stone(self, color, pos):
        circle_color = p.check_color[color]
        pygame.draw.circle(self.display, circle_color, pos, 10)

    def draw_button(self, x, y, counter, buttons):
        i = 0
        for button in buttons:
            if i < int(counter.info):
                button.draw(self.display, x, y + i * 65)
            else:
                b.hide(button, self.display, x, y + i * 65)
            i += 1

    def collect_players(self, counter, switches):
        i = 1
        players = []
        for switch in switches:
            if i <= counter:
                i += 1
                players.append(switch.current_item)
        return players
