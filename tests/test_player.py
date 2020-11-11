from renjuu.game.const import Color
from renjuu.game import game as g
from renjuu.game.player import PlayerEntity, HumanPlayer
from renjuu.game.ai.bot_player import Bot


def test_player_create():
    player = HumanPlayer(Color.black)
    assert player is not None
    assert player.color == Color.black


def test_make_move_to():
    game = g.Game(3, 3, 3, [HumanPlayer(Color.black),
                             Bot(Color.white, PlayerEntity.bot)])
    human_player = game.players[0]
    bot_player = game.players[1]
    x, y = bot_player.make_move(game)
    assert human_player.make_move(game) is None
    assert 0 <= x < 3 and 0 <= y < 3
