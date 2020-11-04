from renjuu.game import board, const
from renjuu.game.const import PlayerEntity, Color
from renjuu.managers.file_manager import json_load, json_save, save
from renjuu.managers.stat_manager import stat_constructor, stat_inc


class Game:
    def __init__(self, width, height, length, players, foul_black):
        self.board = board.Board(width, height, length)
        self.with_foul = foul_black
        self.players = sorted(players, key=lambda player: player.color)
        assert players
        self._player_order = iter(self.players)
        self.current_player = next(self._player_order)
        self.winner = None
        self.max_count_moves = width * height
        self.moves = []

    def switch_players(self):
        try:
            player_to_switch = next(self._player_order)
        except StopIteration:
            self._player_order = iter(self.players)
            player_to_switch = next(self._player_order)
        self.current_player = player_to_switch

    def restart(self):
        self.board.map = self.board.prepare_map()
        self.moves = []
        self.winner = None

    def check_winner(self, v, color):
        if len(self.moves) == self.max_count_moves:
            self.winner = Color.non
        for direction in const.directions:
            length = self.board.find_line(v, direction, color, 1)
            if length >= self.board.length_to_win:
                self.winner = color

    def make_turn(self, v):
        if self.board[v] == Color.non:
            if self.with_foul and self.current_player.color == Color.black\
                    and self.check_foul_move(v):
                return
            else:
                self.board.put_stone(v, self.current_player.color)
                self.moves.append(v)
                self.check_winner(v, self.current_player.color)
                self.switch_players()

    def check_foul_move(self, v):
        lines = []
        fouls = {'forks': [], 'long': []}
        i = 0
        for direction in const.directions:
            length = self.board.find_line(v, direction,
                                          Color.black,
                                          1, fouls=fouls)
            if (length == 3 or length == 4) and fouls['forks'][i]:
                lines.append(length)
            i += 1
        return len(lines) >= 2 or fouls['long'].count(True) >= 1

    def undo_turn(self):
        if not self.moves:
            return
        diff_between_human, color = self._find_diff_between_humans(self.current_player.color)
        for i in range(diff_between_human):
            self.board.put_stone(self.moves[len(self.moves) - 1], Color.non)
            self.moves.pop()
        while self.current_player.color != color:
            self.switch_players()

    def _find_diff_between_humans(self, color):
        last_id = 0
        if color.value == 1:
            diff = 1 + len(self.players)
        else:
            diff = color.value
        for player in self.players:
            if player.entity == PlayerEntity.human:
                if color.value == 1:
                    last_id = player.color.value
                elif last_id < color.value - 1:
                    last_id = player.color.value
        return abs(diff - last_id), Color(last_id)

    def update_stat(self, filename):
        data = json_load(filename + ".json")
        stat_inc(data, self.winner, self.players)
        text = stat_constructor(data)
        json_save(filename + ".json", data)
        save(filename + ".txt", text)
