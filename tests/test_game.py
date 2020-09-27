import unittest
from game import game as g
from game.params import Color


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = g.Game(5, 5, 3)

    def test_game_setup(self):
        self.assertEqual(self.game.board.length_to_win, 3)
        self.assertIsNone(self.game.human_player)
        self.assertIsNotNone(self.game.board)
        self.assertIsNone(self.game.winner)

    def test_prepare_players(self):
        self.game.prepare_players(Color.black)
        self.assertEqual(self.game.human_player.color, Color.black)
        self.assertEqual(self.game.bot_player.color, Color.white)
        self.assertTrue(self.game.is_human_current)

    def test_check_winner(self):
        self.game.prepare_players(Color.black)
        self.game.make_turn(0, 0)
        self.game.make_turn(0, 1)
        self.game.make_turn(0, 2)
        self.game.check_winner(0, 2, Color.black)
        self.assertEqual(self.game.winner, Color.black)

    def test_game_cycle(self):
        self.game.prepare_players(Color.black)
        self.game.turns(0, 0)
        self.game.turns(0, 0)
        if self.game.board.map[0][1] == 0:
            self.game.turns(0, 1)
        else:
            self.game.turns(1, 0)
            self.game.turns(0, 0)
            if self.game.board.map[2][0] == 0:
                self.game.turns(2, 0)
            else:
                self.game.turns(1, 1)
                self.game.turns(0, 0)
                if self.game.board.map[2][2] == 0:
                    self.game.turns(2, 2)
                else:
                    self.game.turns(2, 1)
        self.game.turns(0, 0)
        if self.game.board.map[0][2] == 0:
            self.game.turns(0, 2)
        elif self.game.board.map[1][0] == 0:
            self.game.turns(1, 0)
            self.game.turns(0, 0)
            if self.game.board.map[2][0] == 0:
                self.game.turns(2, 0)
            elif self.game.board.map[1][1] == 0:
                self.game.turns(1, 1)
                self.game.turns(0, 0)
                if self.game.board.map[1][2] == 0:
                    self.game.turns(1, 2)
                elif self.game.board.map[2][1] == 0:
                    self.game.turns(2, 1)
                elif self.game.board.map[2][2] == 0:
                    self.game.turns(2, 2)
                else:
                    self.assertEqual(self.game.winner, Color.white)
                    return
            else:
                self.assertEqual(self.game.winner, Color.white)
                return
        else:
            self.game.turns(1, 1)
            self.game.turns(0, 0)
            if self.game.board.map[2][2] == 0:
                self.game.turns(2, 2)
            else:
                self.game.turns(1, 2)
        self.assertIsNotNone(self.game.winner)


if __name__ == '__main__':
    unittest.main()
