import pytest
from renjuu.game import board as b
from renjuu.game.const import Color, directions
from renjuu.game.vector import Vector


@pytest.fixture()
def board():
    board = b.Board(5, 5, 3)
    board.prepare_map()
    return board


def test_create_board(board):
    assert board.length_to_win == 3
    assert board.width == 5


def test_prepare_map(board):
    board[Vector([0, 0])] = 1
    board[Vector([1, 1])] = 2
    board.map = board.prepare_map()
    assert board.map[0][0] == Color.non and board.map[1][1] == Color.non
    assert len(board.map[0]) == 5


def test_put_stone(board):
    board.put_stone(Vector([0, 0]), Color.white)
    board.put_stone(Vector([1, 1]), Color.white)
    board.put_stone(Vector([2, 2]), Color.white)
    assert board.map[0][0] == Color.white\
        and board.map[1][1] == Color.white \
        and board.map[2][2] == Color.white


@pytest.mark.parametrize("c1, c2, c3, expected", [([0, 0], [0, 1], [0, 2], 3),
                                                  ([0, 0], [1, 1], [2, 2], 3),
                                                  ([0, 0], [1, 0], [2, 0], 3),
                                                  ([0, 0], [0, 2], [0, 1], 3),
                                                  ([1, 0], [2, 0], [0, 0], 3),
                                                  ([1, 1], [0, 0], [2, 2], 3),
                                                  ([0, 4], [0, 3], [0, 2], 3),
                                                  ([3, 3], [4, 4], [2, 2], 3)])
def test_find_line(board, c1, c2, c3, expected):
    board.put_stone(Vector(c1), Color.black)
    board.put_stone(Vector(c2), Color.black)
    board.put_stone(Vector(c3), Color.black)
    for direct in directions:
        length = board.find_line(Vector(c3), direct, Color.black, 1)
        if length == expected:
            assert length == expected
