from renjuu.game import bot_player, board, const, player
from renjuu.game.const import PlayerEntity


class Game:
    def __init__(self, width, height, length, enemy_type):
        self.board = board.Board(width, height, length)
        self.enemy_type = enemy_type
        self.black_player = None
        self.white_player = None
        self.human_player = None
        self.bot_player = None
        self.is_black_current = True
        self.winner = None

    @property
    def current_player(self):
        if self.is_black_current:
            return self.black_player
        else:
            return self.white_player

    def restart(self):
        self.board.prepare_map()
        self.black_player = None
        self.white_player = None
        self.is_black_current = True
        self.winner = None

    def prepare_players(self, color):
        if self.enemy_type == const.GameMode.with_human:
            self.white_player = player.HumanPlayer(const.Color.white)
            self.black_player = player.HumanPlayer(const.Color.black)
            return None
        if color == const.Color.white:
            self.black_player = bot_player.Bot(const.Color.black, PlayerEntity.bot)
            self.white_player = player.HumanPlayer(color)
        if color == const.Color.black:
            self.black_player = player.HumanPlayer(color)
            self.white_player = bot_player.Bot(const.Color.white, PlayerEntity.bot)

    def check_winner(self, x, y, color):
        for direction in const.directions:
            length = self.board.find_line(x, y, direction, color, 1)
            if length >= self.board.length_to_win:
                self.winner = color

    def make_turn(self, x, y):
        if self.board.map[x][y] == 0:
            self.board.put_stone(x, y, self.current_player.color)
            self.check_winner(x, y, self.current_player.color)
            self.is_black_current = not self.is_black_current
