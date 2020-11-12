import pytest

from renjuu.game.ai.bot_player import SmartBot
from renjuu.game.const import Color, PlayerEntity
from renjuu.game.game import Game
from renjuu.game.player import HumanPlayer
from renjuu.game.vector import Vector


@pytest.fixture()
def game():
    return Game(15, 15, 5,
                [HumanPlayer(Color.black),
                 SmartBot(Color.white, PlayerEntity.bot)])


@pytest.fixture()
def bot(game):
    return game.players[1]


@pytest.fixture()
def human(game):
    return game.players[0]


@pytest.mark.parametrize('moves, expected',
                         [([[0, 0], [0, 1], [0, 2], [0, 3]], [0, 4]),
                          ([[14, 0], [14, 1], [14, 2], [14, 3]], [14, 4]),
                          ([[0, 14], [0, 13], [0, 12], [0, 11]], [0, 10]),
                          ([[0, 14], [1, 14], [2, 14], [3, 14]], [4, 14]),
                          ([[0, 0], [1, 0], [2, 0], [3, 0]], [4, 0]),
                          ([[0, 0], [0, 1], [0, 3], [0, 4]], [0, 2]),
                          ([[14, 0], [14, 1], [14, 3], [14, 4]], [14, 2]),
                          ([[0, 14], [0, 13], [0, 11], [0, 10]], [0, 12]),
                          ([[0, 14], [1, 14], [3, 14], [4, 14]], [2, 14]),
                          ([[0, 0], [1, 0], [3, 0], [4, 0]], [2, 0])
                          ])
def test_block_line_with_4(game, bot, moves, expected):
    for move in moves:
        game.make_turn(Vector(move))
        game.make_turn(bot.make_move(game))
    assert game.board[Vector(expected)] == Color.white


@pytest.mark.parametrize('moves, expected',
                         [([[1, 2], [1, 3], [2, 1], [3, 1]], [2, 2]),
                          ([[2, 3], [2, 2], [4, 4], [3, 4], [5, 4]], [2, 4]),
                          ([[2, 8], [2, 7], [3, 6], [4, 6], [5, 6]], [2, 6]),
                          ([[5, 8], [6, 7], [8, 7], [9, 8]], [7, 6]),
                          ([[6, 4], [5, 3], [8, 4], [9, 3]], [7, 5]),
                          ([[10, 7], [11, 7], [12, 6], [12, 5], [9, 7]],
                           [12, 7]),
                          ([[12, 3], [12, 2], [11, 1], [10, 1], [12, 4]],
                           [12, 1])])
def test_block_try_block_forks(game, human, bot, moves, expected):
    for move in moves:
        game.board.put_stone(Vector(move), human.color)
    game.switch_players()
    game.make_turn(bot.make_move(game))
    assert game.board[Vector(expected)] == Color.white
