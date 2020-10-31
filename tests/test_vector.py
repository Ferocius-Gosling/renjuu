from renjuu.game.board import Board
from renjuu.game.bot_player import Bot
from renjuu.game.const import Color
from renjuu.game.vector import Vector
import pytest


def test_create_vector():
    v1 = Vector([0, 0])
    assert v1.x == 0
    assert v1.y == 0


@pytest.mark.parametrize("c1, c2", [([1, 1], [1, 1]),
                                    ([0, 0], [0, 0]),
                                    ([1, 2], [1, 2]),
                                    ([2, 1], [2, 1])])
def test_vector_equals(c1, c2):
    v1 = Vector(c1)
    v2 = Vector(c2)
    assert v1 == v2


@pytest.mark.parametrize("c1, c2", [([1, 1], [2, 2]),
                                    ([1, 1], [1, 2]),
                                    ([1, 1], [2, 1]),
                                    ([2, 1], [2, 2])])
def test_vector_not_equals(c1, c2):
    v1 = Vector(c1)
    v2 = Vector(c2)
    assert v1 != v2


@pytest.mark.parametrize("c1, c2, expected",
                                    [([1, 1], [2, 2], Vector([3, 3])),
                                    ([1, 1], [1, 2], Vector([2, 3])),
                                    ([1, 1], [2, 1], Vector([3, 2])),
                                    ([2, 1], [2, 2], Vector([4, 3]))])
def test_add_vector(c1, c2, expected):
    v1 = Vector(c1)
    v2 = Vector(c2)
    assert v1 + v2 == expected


@pytest.mark.parametrize("c1, c2, expected",
                                    [([1, 1], [2, 2], Vector([-1, -1])),
                                    ([1, 1], [1, 2], Vector([0, -1])),
                                    ([1, 1], [2, 1], Vector([-1, 0])),
                                    ([2, 1], [2, 2], Vector([0, -1]))])
def test_sub_vector(c1, c2, expected):
    v1 = Vector(c1)
    v2 = Vector(c2)
    assert v1 - v2 == expected


@pytest.mark.parametrize("v1, expected", [(Vector([1, 1]), Vector([-1, -1])),
                                    (Vector([1, -2]), Vector([-1, 2])),
                                    (Vector([-2, 1]), Vector([2, -1])),
                                    (Vector([-2, -2]), Vector([2, 2]))])
def test_vector_not_equals(v1, expected):
    assert -v1 == expected



