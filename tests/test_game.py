import unittest
import pytest
from renjuu.game import game as g
from renjuu.game.const import Color, GameMode, PlayerEntity
from renjuu.game.player import HumanPlayer
from renjuu.game.vector import Vector


@pytest.fixture()
def two_human_players():
    return [HumanPlayer(Color.black), HumanPlayer(Color.black)]


@pytest.fixture()
def game(two_human_players):
    game = g.Game(5, 5, 3, two_human_players)
    return game


def test_game_init(game):
    assert game.board.length_to_win == 3
    assert game.black_player is not None
    assert game.winner is None


def test_game_init_with_human():
    game = g.Game(5, 5, 3, GameMode.with_human)
    game.prepare_players(Color.black)
    assert game.black_player.entity == PlayerEntity.human
    assert game.white_player.entity == PlayerEntity.human


@pytest.mark.parametrize("test_input, expected",
                         [(Color.black, (PlayerEntity.human, PlayerEntity.bot)),
                         (Color.white, (PlayerEntity.bot, PlayerEntity.human))])
def test_prepare_players(game, test_input, expected):
    game.prepare_players(test_input)
    assert game.black_player.entity == expected[0]
    assert game.white_player.entity == expected[1]
    assert game.is_black_current


@pytest.mark.parametrize("c1, c2, c3, expected", [([0, 0], [0, 1], [0, 2], 3),
                                                  ([0, 0], [1, 1], [2, 2], 3),
                                                  ([0, 0], [1, 0], [2, 0], 3),
                                                  ([0, 0], [0, 2], [0, 1], 3),
                                                  ([1, 0], [2, 0], [0, 0], 3),
                                                  ([1, 1], [0, 0], [2, 2], 3),
                                                  ([0, 4], [0, 3], [0, 2], 3),
                                                  ([3, 3], [4, 4], [2, 2], 3)])
def test_check_winner(game, c1, c2, c3, expected):
    game.board.put_stone(Vector(c1), Color.black)
    game.board.put_stone(Vector(c2), Color.black)
    game.board.put_stone(Vector(c3), Color.black)
    game.check_winner(Vector(c3), Color.black)
    assert game.winner == Color.black


def test_game_cycle(game):
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector([2, 2]))
    game.make_turn(Vector([0, 1]))
    game.make_turn(Vector([2, 1]))
    game.make_turn(Vector([0, 2]))
    assert game.winner == Color.black


def test_game_cycle_with_bot(game):
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector(game.white_player.make_move(game.board)))
    if game.board.map[0][1] == Color.non:
        game.make_turn(Vector([0, 1]))
    else:
        game.make_turn(Vector([1, 0]))
        game.make_turn(Vector(game.white_player.make_move(game.board)))
        if game.board.map[2][0] == Color.non:
            game.make_turn(Vector([2, 0]))
        else:
            game.make_turn(Vector([1, 1]))
            game.make_turn(Vector(*game.white_player.make_move(game.board)))
            if game.board.map[2][2] == Color.non:
                game.make_turn(Vector([2, 2]))
            else:
                game.make_turn(Vector([2, 1]))
    game.make_turn(Vector(game.white_player.make_move(game.board)))
    if game.board.map[0][2] == Color.non:
        game.make_turn(Vector([0, 2]))
    elif game.board.map[1][0] == Color.non:
        game.make_turn(Vector([1, 0]))
        game.make_turn(Vector(game.white_player.make_move(game.board)))
        if game.board.map[2][0] == Color.non:
            game.make_turn(Vector([2, 0]))
        elif game.board.map[1][1] == Color.non:
            game.make_turn(Vector([1, 1]))
            game.make_turn(Vector(game.white_player.make_move(game.board)))
            if game.board.map[1][2] == Color.non:
                game.make_turn(Vector([1, 2]))
            elif game.board.map[2][1] == Color.non:
                game.make_turn(Vector([2, 1]))
            elif game.board.map[2][2] == Color.non:
                game.make_turn(Vector([2, 2]))
            else:
                assert game.winner == Color.white
                return
        else:
            assert game.winner == Color.white
            return
    else:
        game.make_turn(Vector([1, 1]))
        game.make_turn(Vector(game.white_player.make_move(game.board)))
        if game.board.map[2][2] == Color.non:
            game.make_turn(Vector([2, 2]))
        else:
            game.make_turn(Vector([1, 2]))
    assert game.winner == Color.black


def test_restart_game(game):
    game.restart()
    assert game.winner is None
    assert game.is_black_current
    assert game.black_player is None


if __name__ == '__main__':
    unittest.main()
