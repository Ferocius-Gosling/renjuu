from renjuu.game.const import Color
from renjuu.game import board as b
from renjuu.game.player import PlayerEntity, HumanPlayer
from renjuu.game.bot_player import Bot


def test_player_create():
    player = HumanPlayer(Color.black)
    assert player is not None
    assert player.color == Color.black


def test_make_move_to():
    board = b.Board(3, 3, 3)
    human_player = HumanPlayer(Color.black)
    bot_player = Bot(Color.white, PlayerEntity.bot)
    x, y = bot_player.make_move(board)
    assert human_player.make_move(board) is None
    assert 0 <= x < 3 and 0 <= y < 3
