import pytest
from renjuu.game import board as b
from renjuu.game.const import Color, directions


@pytest.fixture()
def board():
    board = b.Board(5, 5, 3)
    board.prepare_map()
    return board


def test_create_board(board):
    assert board.length_to_win == 3
    assert board.width == 5


def test_prepare_map(board):
    board[0][0] = 1
    board[1][1] = 2
    board.map = board.prepare_map()
    assert board[0][0] == 0 and board[1][1] == 0
    assert len(board[0]) == 5


def test_put_stone(board):
    board.put_stone(0, 0, Color.white)
    board.put_stone(1, 1, Color.white)
    board.put_stone(2, 2, Color.white)
    assert board[0][0] == Color.white.value\
        and board[1][1] == Color.white.value \
        and board[2][2] == Color.white.value


@pytest.mark.parametrize("test_input, expected", [([(0, 0), (0, 1), (0, 2)], 3),
                                                  ([(0, 0), (1, 1), (2, 2)], 3),
                                                  ([(0, 0), (1, 0), (2, 0)], 3),
                                                  ([(0, 0), (0, 2), (0, 1)], 3),
                                                  ([(1, 0), (2, 0), (0, 0)], 3),
                                                  ([(1, 1), (0, 0), (2, 2)], 3),
                                                  ([(0, 4), (0, 3), (0, 2)], 3),
                                                  ([(3, 3), (4, 4), (2, 2)], 3)])
def test_find_line(board, test_input, expected):
    board.put_stone(test_input[0][0], test_input[0][1], Color.black)
    board.put_stone(test_input[1][0], test_input[1][1], Color.black)
    board.put_stone(test_input[2][0], test_input[2][1], Color.black)
    for direct in directions:
        length = board.find_line(test_input[2][0], test_input[2][1], direct, Color.black, 1)
        if length == expected:
            assert length == expected
