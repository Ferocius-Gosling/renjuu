import unittest
from game.params import Color
from game import player as p
from game import board as b


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.first_player = p.Player(Color.black)
        self.second_player = p.Player(Color.white)
        self.board = b.Board(5, 5, 3)

    def test_player_create(self):
        player = p.Player(1)
        self.assertIsNotNone(player)
        self.assertEqual(player.color, 1)

    def test_make_move_to(self):
        self.first_player.make_move(self.board, 0, 0)
        self.second_player.make_move(self.board, 1, 1)
        self.assertEqual(self.board.map[0][0], 1)
        self.assertEqual(self.board.map[1][1], 2)


if __name__ == '__main__':
    unittest.main()
