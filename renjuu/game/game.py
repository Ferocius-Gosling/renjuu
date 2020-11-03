from renjuu.game import bot_player, board, const, player
from renjuu.game.const import PlayerEntity, Color
from renjuu.game.vector import Vector


class Game:
    def __init__(self, width, height, length, players):
        self.board = board.Board(width, height, length)
        self.players = sorted(players, key=lambda player: player.color)
        assert players
        self._player_order = iter(self.players)
        self.current_player = next(self._player_order)
        self.winner = None

    def switch_players(self):
        try:
            player_to_switch = next(self._player_order)
        except StopIteration:
            self._player_order = iter(self.players)
            player_to_switch = next(self._player_order)
        self.current_player = player_to_switch

    def restart(self):
        self.board.map = self.board.prepare_map()
        self.winner = None

    def check_winner(self, v, color):
        for direction in const.directions:
            length = self.board.find_line(v, direction, color, 1)
            if length >= self.board.length_to_win:
                self.winner = color

    def make_turn(self, v):
        if self.board[v] == Color.non:
            self.board.put_stone(v, self.current_player.color)
            self.check_winner(v, self.current_player.color)
            self.switch_players()
