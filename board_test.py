from board import Board

import unittest


class MyTestCase(unittest.TestCase):
    def test_is_bomb_true(self):
        test_board = Board()
        test_board.grid[1].is_bomb = True
        self.assertEqual(test_board.check_cell(1)['is_bomb'], True)

    def test_is_bomb_false(self):
        test_board = Board()
        test_board.grid[1].is_bomb = False
        self.assertEqual(test_board.check_cell(1)['is_bomb'], False)

    def test_is_covered_true(self):
        test_board = Board()
        test_board.grid[5].is_covered = True
        self.assertEqual(test_board.check_cell(5)['is_covered'], True)

    def test_is_covered_false(self):
        test_board = Board()
        test_board.grid[5].is_covered = False
        self.assertEqual(test_board.check_cell(5)['is_covered'], False)

    def test_is_board_empty(self):
        test_board = Board()
        test_board.NUMBER_OF_FREE_TILES = 0
        self.assertEqual(test_board.check_cell(5)['is_board_empty'], True)


if __name__ == '__main__':
    unittest.main()
