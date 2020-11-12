from renjuu.game.game import Game
from renjuu.game import params as game_params, const
from renjuu.game.player import HumanPlayer
from renjuu.game.ai.bot_player import RandomBot, SmartBot
from renjuu.game.scoreboard import Scoreboard
from renjuu.game.vector import Vector
from renjuu.view import params as view_params, button
from renjuu.view.click_handler import ClickHandler
from renjuu.view.utils import get_coordinates
import pygame


class MainWindow:
    def __init__(self):
        self.game = None
        self.scoreboard = Scoreboard("scores")
        self.display = pygame.display.set_mode((view_params.screen_width,
                                                view_params.screen_height))
        self.display.fill(view_params.menu_color)
        self.clock = pygame.time.Clock()

    def open_start_menu(self):
        start_button = button.Button(100, 65, view_params.board_color)
        start_button.draw(self.display, view_params.screen_width // 2.5,
                          view_params.screen_height // 2)
        self.clock.tick(15)
        launching = True
        while launching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launching = False
            pygame.display.update()

    def open_settings_menu(self):
        self.display.fill(view_params.menu_color)
        counter = button.CounterWithLimits(8, 2)
        buttons = []
        start_button = button.Button(120, 70, view_params.black_color)
        player_counter_button = button.Button(120, 70, view_params.menu_color,
                                              info="2")
        inc_button = button.Button(50, 70, view_params.white_color)
        dec_button = button.Button(50, 70, view_params.white_color)
        foul_button = button.SwitchButton(120, 80,
                                          [view_params.menu_color,
                                           view_params.menu_color],
                                          ["Without foul", "With foul"],
                                          [False, True])
        switches = []
        i = 1
        for color in view_params.colors:
            buttons.append(button.SwitchButton(50, 50,
                                               [color,
                                                view_params.menu_color],
                                               [None, None],
                                               [const.Color(i),
                                                const.Color(i)]))
            i += 1
        for i in range(8):
            switches.append(button.SwitchButton(
                100, 50,
                [view_params.menu_color,
                 view_params.menu_color,
                 view_params.menu_color],
                ["Human", "Random bot", "Smart bot"],
                [HumanPlayer(buttons[i].current_item),
                 RandomBot(buttons[i].current_item, const.PlayerEntity.bot),
                 SmartBot(buttons[i].current_item, const.PlayerEntity.bot)]))
        choice = True
        while choice:
            self.draw_button(75, 50, player_counter_button, buttons)
            self.draw_button(140, 50, player_counter_button, switches)
            player_counter_button.draw(self.display, 300, 100)
            inc_button.draw(self.display, 240, 100, player_counter_button,
                            action=counter.button_value_increment_with_limit)
            dec_button.draw(self.display, 400, 100, player_counter_button,
                            action=counter.button_value_decrement_with_limit)
            start_button.draw(self.display, 570, 300)
            foul_button.draw(self.display, 300, 200)
            # difficult_button.draw(self.display, 300, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choice = False
            if start_button.is_pressed:
                choice = False
                self.game_on_board(self.collect_players(
                    int(player_counter_button.info), switches),
                    foul_button.current_item)
            pygame.display.update()

    def game_on_board(self, players, with_foul):
        self.game = Game(game_params.board_width, game_params.board_height,
                         game_params.length_to_win,
                         players, with_foul)
        game_params.PLAYER_COUNT = len(self.game.players)
        self.display.blit(view_params.board_back, (0, 0))
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
            if current_player.entity == const.PlayerEntity.human:
                if click_handler.check_click(click_pos, click):
                    if click_handler.handle() is not None:
                        x, y = click_handler.handle()
                        self.game.make_turn(Vector([x, y]))
                    else:
                        continue
            else:
                x, y = current_player.make_move(self.game)
                self.game.make_turn(Vector([x, y]))
            if pygame.key.get_pressed()[pygame.K_z]:
                self.game.undo_turn()
                pygame.time.wait(150)
                self.clear()
            if self.game.winner is not None:
                pygame.time.wait(150)
                cycle = False
                self.scoreboard.update_stat(self.game)
                self.end_game()
            self.update_map()
            pygame.display.update()

    def end_game(self):
        self.display.fill(view_params.board_color)
        again_button = button.Button(120, 70, view_params.blue_color)
        quit_button = button.Button(120, 70, view_params.red_color)
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
                if self.game.board.map[i][j] != const.Color.non:
                    self.draw_stone(self.game.board.map[i][j],
                                    get_coordinates(i, j))

    def clear(self):
        self.display.blit(view_params.board_back, (0, 0))

    def draw_stone(self, color, pos):
        circle_color = view_params.check_color[color]
        pygame.draw.circle(self.display, circle_color, pos, 10)

    def draw_button(self, x, y, counter, buttons):
        i = 0
        for control in buttons:
            if i < int(counter.info):
                control.draw(self.display, x, y + i * 65)
            else:
                control.hide(self.display, x, y + i * 65)
            i += 1

    def collect_players(self, counter, switches):
        i = 1
        players = []
        for switch in switches:
            if i <= counter:
                i += 1
                players.append(switch.current_item)
        return players
