from renjuu.game.game import Game
from renjuu.game import params as game_params, const
from renjuu.game.player import HumanPlayer
from renjuu.game.ai.bot_player import RandomBot, SmartBot
from renjuu.game.scoreboard import Scoreboard
from renjuu.game.vector import Vector
from renjuu.network.const import RequestParams, RequestType
from renjuu.view import params as view_params, button
from renjuu.view.click_handler import ClickHandler
from renjuu.view.utils import get_coordinates
from renjuu.network.server import GameServer
from renjuu.network.params import load_settings
from renjuu.network.client import GameClient
import pygame


class MainWindow:
    def __init__(self):
        self.game = None
        self.scoreboard = Scoreboard("scores")
        self.display = pygame.display.set_mode((view_params.screen_width,
                                                view_params.screen_height))
        self.display.fill(view_params.menu_color)
        self.clock = pygame.time.Clock()
        self.game_server = None
        self.game_client = None

    def open_start_menu(self):
        self.display.fill(view_params.menu_color)
        single_player_button = button.Button(150, 65, view_params.board_color,
                                             info='Hot-seat or bots')
        multiplayer_button = button.Button(150, 65, view_params.board_color,
                                           info='Multiplayer')
        self.clock.tick(15)
        launching = True
        while launching:
            single_player_button.draw(self.display, 200, 100)
            multiplayer_button.draw(self.display, 200, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launching = False
                    pygame.quit()
            if single_player_button.is_pressed:
                launching = False
                self.open_settings_menu()
            if multiplayer_button.is_pressed:
                launching = False
                self.open_multiplayer_menu()
            pygame.display.update()

    def open_multiplayer_menu(self):
        self.display.fill(view_params.menu_color)
        start_server_button = button.Button(120, 80, view_params.board_color,
                                            info='Create room')
        connect_to_button = button.Button(120, 80, view_params.board_color,
                                          info='Connect to room')
        back_to_start_button = button.Button(120, 80, view_params.board_color,
                                             info='Back to menu')
        self.clock.tick(15)
        launching = True
        while launching:
            start_server_button.draw(self.display, 440, 200)
            connect_to_button.draw(self.display, 440, 310)
            back_to_start_button.draw(self.display, 340, 420)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launching = False
            if start_server_button.is_pressed:
                launching = False
                self.open_multiplayer_settings()
            if connect_to_button.is_pressed:
                launching = False
                client_params = load_settings('network.json')
                self.game_client = GameClient(client_params['conn-ip'],
                                              client_params['conn-port'])
                self.game_client.connect_server(client_params['name'])
                self.open_multiplayer_lobby()
            if back_to_start_button.is_pressed:
                launching = False
                self.open_start_menu()
            pygame.display.update()

    def open_multiplayer_settings(self):
        self.display.fill(view_params.menu_color)
        counter = button.CounterWithLimits(8, 2)
        start_button = button.Button(120, 70, view_params.black_color)
        inc_button = button.Button(50, 70, view_params.white_color)
        dec_button = button.Button(50, 70, view_params.white_color)
        player_counter_button = button.Button(120, 70, view_params.menu_color,
                                              info="2")
        self.clock.tick(15)
        launching = True
        while launching:
            player_counter_button.draw(self.display, 300, 100)
            inc_button.draw(self.display, 240, 100, player_counter_button,
                            action=counter.button_value_increment_with_limit)
            dec_button.draw(self.display, 400, 100, player_counter_button,
                            action=counter.button_value_decrement_with_limit)
            start_button.draw(self.display, 570, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launching = False
            if start_button.is_pressed:
                launching = False
                connecting_params = load_settings('network.json')
                self.game_server = GameServer(connecting_params['self-ip'],
                                              connecting_params['self-port'],
                                              int(player_counter_button.info))
                self.game_client = GameClient(connecting_params['self-ip'],
                                              connecting_params['self-port'])
                self.game_client.connect_server(connecting_params['name'])
                self.open_multiplayer_lobby()
            pygame.display.update()

    def open_multiplayer_lobby(self):
        self.display.fill(view_params.menu_color)
        i = 1
        colors = []
        player_buttons = []
        if self.game_client.message_monitor.max_players is None:
            pygame.time.wait(50)
        start_button = button.Button(100, 60, view_params.black_color)
        max_players_button = button.Button(1, 1, view_params.menu_color,
                                           info=self.game_client
                                           .message_monitor.max_players)
        for color in view_params.colors:
            if i > self.game_client.message_monitor.max_players:
                continue
            colors.append(button.Button(50, 50, color))
            i += 1
        for i in range(self.game_client.message_monitor.max_players):
            if i < len(self.game_client.message_monitor.player_params):
                player_param = self.game_client.message_monitor\
                    .player_params[i]
                player_buttons\
                    .append(button.Button(100, 50,
                                          view_params.menu_color,
                                          info=player_param
                                          [RequestParams.NAME]))
            else:
                player_buttons.append(button.Button(100, 50,
                                                    view_params.menu_color,
                                                    info='None'))
        waiting_for_players = True
        self.game_client.message_monitor.start_button = start_button
        message = {RequestParams.TYPE: RequestType.BEGIN,
                   RequestParams.ID: self.game_client.message_monitor.id}
        while waiting_for_players:
            self.draw_button(75, 50, max_players_button, colors)
            self.draw_button(140, 50, max_players_button, player_buttons)
            self.refresh_button_info(player_buttons)
            start_button.draw(self.display, 370, 300, action=None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_players = False
                    self.game_client.close_event()
                    if self.game_server is not None:
                        self.game_server.close()
            if start_button.is_pressed:
                if self.game_client is not None:
                    self.game_client.send_message(message)
                    if self.game_client.message_monitor\
                            .request[RequestParams.ID] != 1:
                        continue
                waiting_for_players = False
                self.game_on_board(self.collect_players_from_button(
                    player_buttons), False)
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
        if self.game_client is not None:
            self.game_client.message_monitor.game = self.game
        self.display.blit(view_params.board_back, (0, 0))
        pygame.time.wait(200)
        click_handler = ClickHandler()
        cycle = True
        self.clock.tick(20)
        while cycle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False
                    if self.game_client is not None:
                        self.game_client.close_event()
                        if self.game_server is not None:
                            pygame.time.wait(100)
                            self.game_server.close()
                            self.game_server = None
                    pygame.quit()
            click_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            current_player = self.game.current_player
            if current_player.entity == const.PlayerEntity.human:
                if click_handler.check_click(click_pos, click):
                    if click_handler.handle() is not None:
                        x, y = click_handler.handle()
                        if self.game_client is not None:
                            if current_player.color.value \
                                    == self.game_client.message_monitor.id:
                                message = {RequestParams.TYPE:
                                           RequestType.MOVE,
                                           RequestParams.ID:
                                               current_player.color.value,
                                           RequestParams.MOVE: (x, y)}
                                if self.game.board[Vector([x, y])] \
                                        == const.Color.non:
                                    self.game_client.send_message(message)
                                    self.game.make_turn(Vector([x, y]))
                        else:
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
        restart_button = button.Button(120, 70, view_params.blue_color)
        quit_button = button.Button(120, 70, view_params.red_color)
        game_over = True
        message = {RequestParams.TYPE: RequestType.RESTART,
                   RequestParams.ID: self.game_client.message_monitor.id}
        if self.game_client is not None:
            self.game_client.message_monitor.restart_button = restart_button
        while game_over:
            restart_button.draw(self.display, 230, 200, action=None)
            quit_button.draw(self.display, 470, 200, action=None)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    if self.game_client is not None:
                        self.game_client.close_event()
                        self.game_client = None
                        if self.game_server is not None:
                            pygame.time.wait(100)
                            self.game_server.close()
                            self.game_server = None
            if restart_button.is_pressed:
                if self.game_client is not None:
                    self.game_client.send_message(message)
                    if self.game_client.message_monitor\
                            .request[RequestParams.ID] != 1:
                        continue
                game_over = False
                self.game.restart()
                if self.game_client is not None:
                    self.game_client.close_event()
                    self.game_client = None
                    if self.game_server is not None:
                        pygame.time.wait(100)
                        self.game_server.close()
                        self.game_server = None
                    self.open_start_menu()
                self.open_start_menu()
            if quit_button.is_pressed:
                game_over = False
                if self.game_client is not None:
                    self.game_client.close_event()
                    if self.game_server is not None:
                        pygame.time.wait(100)
                        self.game_server.close()
                        self.game_server = None
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

    def collect_players_from_button(self, buttons):
        players = []
        for i in range(len(buttons)):
            players.append(HumanPlayer(const.Color(i+1),
                                       name=buttons[i].info))
        return players

    def refresh_button_info(self, buttons):
        i = 0
        for control in buttons:
            if i < len(self.game_client.message_monitor.player_params):
                name = self.game_client.message_monitor \
                    .player_params[i][RequestParams.NAME]
                control.info = name
            i += 1
