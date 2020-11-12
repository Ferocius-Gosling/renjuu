import pytest
import os

from renjuu.game.game import Game
from renjuu.game.scoreboard import Scoreboard
from renjuu.game.const import Color
from renjuu.game.player import HumanPlayer


@pytest.fixture()
def data():
    return {"black": 1, "white": 2}


@pytest.fixture()
def scoreboard():
    return Scoreboard("test")


def test_json_save_and_load(scoreboard, data):
    scoreboard.json_save('test', data)
    data = scoreboard.json_load('test')
    assert data is not None
    assert os.path.exists("test")
    assert data['black'] == 1
    assert data['white'] == 2
    os.remove('test')


def test_save_file(scoreboard):
    scoreboard.save('test_save', 'test')
    assert os.path.exists('test_save')
    os.remove('test_save')


def test_stat_construct(scoreboard, data):
    text = scoreboard.parse_data(data)
    assert text == "Score table\nblack : 1 \nwhite : 2 \n"


def test_stat_inc(scoreboard, data):
    temp1 = data['black']
    temp2 = data['white']
    scoreboard.stat_increment(data, Color.non,
                [HumanPlayer(Color.black), HumanPlayer(Color.white)])
    assert temp1 + 1 == data['black']
    assert temp2 + 1 == data['white']


def test_update_stat():
    game = Game(3, 3, 3, [HumanPlayer(Color.black),
                          HumanPlayer(Color.white)])
    game.winner = Color.white
    scoreboard = Scoreboard("test_update")
    scoreboard.update_stat(game)
    assert os.path.exists("test_update.json")
    assert os.path.exists("test_update.txt")
    result = scoreboard.json_load("test_update.json")
    assert result[Color.black.name] == 0
    assert result[Color.white.name] == 2
    os.remove("test_update.txt")
    os.remove("test_update.json")
