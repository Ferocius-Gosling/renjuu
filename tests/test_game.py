import os
import unittest
import pytest
from renjuu.game import game as g
from renjuu.game.ai.bot_player import RandomBot
from renjuu.game.const import Color, PlayerEntity
from renjuu.game.player import HumanPlayer
from renjuu.game.vector import Vector


@pytest.fixture()
def two_human_players():
    return [HumanPlayer(Color.black), HumanPlayer(Color.white)]


@pytest.fixture()
def bot_and_human_players():
    return [HumanPlayer(Color.black), RandomBot(Color.white, PlayerEntity.bot)]


@pytest.fixture()
def game(two_human_players):
    game = g.Game(5, 5, 3, two_human_players)
    return game


def test_game_init(game):
    assert game.board.length_to_win == 3
    assert game.players is not None
    assert game.winner is None


def test_game_init_with_human(two_human_players):
    game = g.Game(5, 5, 3, two_human_players)
    assert game.players[0].color == Color.black
    assert game.players[1].color == Color.white


@pytest.mark.parametrize("test_input, expected",
            [([HumanPlayer(Color.red), HumanPlayer(Color.white), HumanPlayer(Color.black)],
            [Color.black, Color.white, Color.red]),
            ([HumanPlayer(Color.gray), HumanPlayer(Color.green), HumanPlayer(Color.yellow)],
            [Color.yellow, Color.green, Color.gray])])
def test_sorted_players(test_input, expected):
    game = g.Game(5, 5, 3, test_input)
    assert game.players[0].color == expected[0]
    assert game.players[1].color == expected[1]
    assert game.players[2].color == expected[2]
    assert game.current_player.color == expected[0]


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


def test_check_draw(two_human_players):
    game = g.Game(3, 3, 4, two_human_players)
    for i in range(game.board.width):
        for j in range(game.board.height):
            game.make_turn(Vector([i, j]))
    assert game.winner == Color.non


def test_game_cycle(game):
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector([2, 2]))
    game.make_turn(Vector([0, 1]))
    game.make_turn(Vector([2, 1]))
    game.make_turn(Vector([0, 2]))
    assert game.winner == Color.black


@pytest.mark.parametrize("players, expected",
                    [([HumanPlayer(Color.white), HumanPlayer(Color.black)], Color.black),
                     ([HumanPlayer(Color.black), HumanPlayer(Color.white), HumanPlayer(Color.red)],
                     Color.red),
                     ([HumanPlayer(Color.black), HumanPlayer(Color.white),
                       RandomBot(Color.red, PlayerEntity.bot)], Color.white),
                     ([HumanPlayer(Color.black), RandomBot(Color.white, PlayerEntity.bot),
                       RandomBot(Color.red, PlayerEntity.bot)], Color.black),
                     ([HumanPlayer(Color.black), RandomBot(Color.white, PlayerEntity.bot),
                       HumanPlayer(Color.red)], Color.red),
                     ([RandomBot(Color.black, PlayerEntity.bot), HumanPlayer(Color.white),
                       HumanPlayer(Color.red, PlayerEntity.bot)], Color.white)
                     ])
def test_undo_moves(players, expected):
    game = g.Game(5, 5, 3, players)
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector([0, 1]))
    game.make_turn(Vector([0, 2]))
    game.undo_turn()
    assert game.current_player.color == expected
    assert game.board[0, 2] == Color.non


def test_undo_when_no_to_undo(game):
    try:
        game.undo_turn()
    except IndexError:
        assert False
    finally:
        assert True


def test_check_fouls_forks(two_human_players):
    game = g.Game(5, 5, 5, two_human_players, True)
    game.make_turn(Vector([3, 1]))
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector([3, 2]))
    game.make_turn(Vector([0, 1]))
    game.make_turn(Vector([1, 3]))
    game.make_turn(Vector([1, 0]))
    game.make_turn(Vector([2, 3]))
    game.make_turn(Vector([1, 1]))
    game.make_turn(Vector([3, 3]))
    assert game.board[Vector([3, 3])] == Color.non


def test_check_fouls_long(two_human_players):
    game = g.Game(10, 10, 5, two_human_players, True)
    game.make_turn(Vector([1, 3]))
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector([2, 3]))
    game.make_turn(Vector([0, 1]))
    game.make_turn(Vector([3, 3]))
    game.make_turn(Vector([1, 0]))
    game.make_turn(Vector([5, 3]))
    game.make_turn(Vector([1, 1]))
    game.make_turn(Vector([6, 3]))
    game.make_turn(Vector([9, 9]))
    game.make_turn(Vector([4, 3]))
    assert game.board[Vector([4, 3])] == Color.non


def test_game_cycle_with_bot(bot_and_human_players):
    game = g.Game(5, 5, 3, bot_and_human_players)
    game.make_turn(Vector([0, 0]))
    game.make_turn(Vector(game.current_player.make_move(game)))
    if game.board.map[0][1] == Color.non:
        game.make_turn(Vector([0, 1]))
    else:
        game.make_turn(Vector([1, 0]))
        game.make_turn(Vector(game.current_player.make_move(game)))
        if game.board.map[2][0] == Color.non:
            game.make_turn(Vector([2, 0]))
        else:
            game.make_turn(Vector([1, 1]))
            game.make_turn(Vector(game.current_player.make_move(game)))
            if game.board.map[2][2] == Color.non:
                game.make_turn(Vector([2, 2]))
            else:
                game.make_turn(Vector([2, 1]))
    game.make_turn(Vector(game.current_player.make_move(game)))
    if game.board.map[0][2] == Color.non:
        game.make_turn(Vector([0, 2]))
    elif game.board.map[1][0] == Color.non:
        game.make_turn(Vector([1, 0]))
        game.make_turn(Vector(game.current_player.make_move(game)))
        if game.board.map[2][0] == Color.non:
            game.make_turn(Vector([2, 0]))
        elif game.board.map[1][1] == Color.non:
            game.make_turn(Vector([1, 1]))
            game.make_turn(Vector(game.current_player.make_move(game)))
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
        game.make_turn(Vector(game.current_player.make_move(game)))
        if game.board.map[2][2] == Color.non:
            game.make_turn(Vector([2, 2]))
        else:
            game.make_turn(Vector([1, 2]))
    assert game.winner == Color.black


def test_restart_game(game):
    game.restart()
    assert game.winner is None
    assert game.board[0, 0] == Color.non


if __name__ == '__main__':
    unittest.main()
