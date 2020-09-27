from game import board, player, params, bot, point


class Game:
    def __init__(self, width, height, length):
        self.board = board.Board(width, height, length)
        self.human_player = None
        self.bot_player = None
        self.game_stage = params.GameStage.game_settings
        self.is_human_current = True
        self.winner = None

    def restart(self):
        self.board = board.Board(self.board.width,
                                 self.board.height,
                                 self.board.length_to_win)
        self.human_player = None
        self.bot_player = None
        self.game_stage = params.GameStage.game_settings
        self.is_human_current = True
        self.winner = None

    def prepare_players(self, color):
        if color == params.Color.white:
            self.is_human_current = False
            self.bot_player = bot.Bot(params.Color.black)
            self.human_player = player.Player(color)
        if color == params.Color.black:
            self.human_player = player.Player(color)
            self.bot_player = bot.Bot(params.Color.white)

    def check_winner(self, x, y, color):
        directions = self.board.check_around(x, y, color)
        for direction in directions:
            second_dir = self.board.find_second_dir(direction, directions)
            self.winner = self.board.find_line(x, y, color, direction, second_dir)
            if self.winner is not None:
                break

    def make_turn(self, x, y):
        if self.board.map[x][y] == 0:
            self.human_player.make_move(self.board, x, y)
            self.is_human_current = not self.is_human_current
            self.check_winner(x, y, self.human_player.color)

    def bot_make_turn(self):
        x, y = self.bot_player.make_move(self.board)
        self.is_human_current = not self.is_human_current
        self.check_winner(x, y, self.bot_player.color)

    def turns(self, x, y):
        if self.is_human_current:
            self.make_turn(x, y)
        else:
            self.bot_make_turn()

    def change_stage(self, stage):
        self.game_stage = stage
