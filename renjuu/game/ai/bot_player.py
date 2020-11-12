import random

from renjuu.game.ai.checkers import count_weight
from renjuu.game.const import Color
from renjuu.game.player import Player
from renjuu.game.vector import Vector


class RandomBot(Player):
    def make_move(self, game):
        if not game.smart_bot:
            x = random.randint(0, game.board.width - 1)
            y = random.randint(0, game.board.height - 1)
            vec = Vector([x, y])
            while game.board[vec] != Color.non:
                x = random.randint(0, game.board.width - 1)
                y = random.randint(0, game.board.height - 1)
                vec = Vector([x, y])
            return x, y


class SmartBot(Player):
    def make_move(self, game):
        weights_table = {}
        for x in range(game.board.width):
            for y in range(game.board.height):
                vector = Vector([x, y])
                if game.board[vector] != Color.non:
                    continue
                weights_table[vector] = count_weight(game, vector)
        values = list(weights_table.values())
        keys = list(weights_table.keys())
        return keys[values.index(max(values))]

