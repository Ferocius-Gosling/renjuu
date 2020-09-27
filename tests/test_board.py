import unittest
from game import board as b
from game.params import Color


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = b.Board(5, 5, 3)

    def test_create_board(self):
        board = b.Board(5, 5, 3)
        self.assertEqual(board.width, 5)
        self.assertEqual(board.height, 5)
        self.assertEqual(board.length_to_win, 3)

    def test_prepare_map(self):
        board = b.Board(5, 5, 3)
        board.map[0][0] = 1
        board.map[1][1] = 2
        board.map = board.prepare_map()
        self.assertEqual(board.map[0][0], 0)
        self.assertEqual(board.map[1][1], 0)

    def test_check_around(self):
        self.board.prepare_map()
        self.board.map[0][0] = 1
        self.board.map[0][1] = 1
        direction = self.board.check_around(0, 1, Color.black)
        self.assertEqual(len(direction), 1)
        self.assertTupleEqual(direction[0], (0, -1))

    def test_check_around_diff_colors(self):
        self.board.prepare_map()
        for i in range(3):
            for j in range(3):
                if i == j == 1:
                    continue
                self.board.map[i][j] = 2
        self.board.map[1][1] = 1
        direction = self.board.check_around(1, 1, Color.black)
        self.assertEqual(len(direction), 0)

    def test_check_around_some_colors(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[i][0] = 2
        for i in range(3):
            self.board.map[i][1] = 1
        dirs = self.board.check_around(1, 1, Color.black)
        self.assertEqual(len(dirs), 2)
        self.assertTrue(dirs.__contains__((-1, 0)))
        self.assertTrue(dirs.__contains__((1, 0)))

    def test_check_around_diagonal(self):
        self.board.prepare_map()
        for i in [0, 2]:
            for j in [0, 2]:
                self.board.map[i][j] = 1
        self.board.map[1][1] = 1
        dirs = self.board.check_around(1, 1, Color.black)
        for i in [-1, 1]:
            for j in [-1, 1]:
                self.assertTrue(dirs.__contains__((i, j)))

    def test_build_line_horizontal(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[i][0] = 1
        length = self.board.build_line(2, 0, Color.black, (-1, 0), 1)
        self.assertEqual(length, 3)

    def test_build_line_vertical(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[0][i] = 1
        length = self.board.build_line(0, 2, Color.black, (0, -1), 1)
        self.assertEqual(length, 3)

    def test_build_line_diagonal(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[i][i] = 1
        length = self.board.build_line(0, 0, Color.black, (1, 1), 1)
        self.assertEqual(length, 3)

    def test_build_line_diff_color(self):
        self.board.prepare_map()
        for i in range(2):
            self.board.map[i+1][i+1] = 1
        self.board.map[0][0] = 2
        length = self.board.build_line(2, 2, Color.black, (-1, -1), 1)
        self.assertEqual(length, 2)

    def test_find_line(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[i][0] = 1
        color = self.board.find_line(2, 0, Color.black, (-1, 0), None)
        self.assertEqual(color, Color.black)

    def test_find_line_between_points(self):
        self.board.prepare_map()
        for i in range(3):
            self.board.map[i][0] = 1
        color = self.board.find_line(1, 0, Color.black, (-1, 0), (1, 0))
        self.assertEqual(color, Color.black)

    def test_find_second_dir(self):
        second_dir = b.Board.find_second_dir((1,0), [(1,0),(0,1),(-1,0)])
        self.assertTupleEqual(second_dir, (-1, 0))

    def test_find_second_dir_diagonal1(self):
        second_dir = b.Board.find_second_dir((1,1), [(1,0),(0,1),(-1,-1)])
        self.assertTupleEqual(second_dir, (-1, -1))

    def test_find_second_dir_diagonal2(self):
        second_dir = b.Board.find_second_dir((1,-1), [(1,0),(0,1),(-1,1)])
        self.assertTupleEqual(second_dir, (-1, 1))

    def test_no_find_second_dir(self):
        second_dir = b.Board.find_second_dir((1, 1), [(1, 0), (0, 1), (-1, 1)])
        self.assertIsNone(second_dir)


if __name__ == '__main__':
    unittest.main()
