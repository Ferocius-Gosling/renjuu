import pytest
import renjuu.managers.stat_manager as sm
import renjuu.managers.file_manager as fm
import os

from renjuu.game.const import Color
from renjuu.game.player import HumanPlayer


@pytest.fixture()
def data():
    return {"black": 1, "white": 2}


def test_json_save_and_load(data):
    fm.json_save('test', data)
    data = fm.json_load('test')
    assert data is not None
    assert os.path.exists("test")
    assert data['black'] == 1
    assert data['white'] == 2
    os.remove('test')


def test_save_file():
    fm.save('test_save', 'test')
    assert os.path.exists('test_save')
    os.remove('test_save')


def test_stat_construct(data):
    text = sm.stat_constructor(data)
    assert text == "Score table\nblack : 1 \nwhite : 2 \n"


def test_stat_inc(data):
    temp1 = data['black']
    temp2 = data['white']
    sm.stat_inc(data, Color.non,
                [HumanPlayer(Color.black), HumanPlayer(Color.white)])
    assert temp1 + 1 == data['black']
    assert temp2 + 1 == data['white']
