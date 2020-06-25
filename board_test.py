import unittest
import board
import settings

class BoardTest(unittest.TestCase):

    def test_is_bomb_true(self):
        test_board = board.Board()
        test_board.grid[1].is_bomb = True
        status = test_board.check_cell(1)
        self.assertEqual(status.is_bomb, 'True')

    def test_is_bomb_false(self):
        test_board = board.Board()
        test_board.grid[1].is_bomb = False
        self.assertEqual(test_board.check_cell(1).is_bomb, 'False')

    def test_is_covered_true(self):
        test_board = board.Board()
        test_board.grid[5].is_covered = True
        self.assertEqual(test_board.check_cell(5).is_covered, 'True')

    def test_is_covered_false(self):
        test_board = board.Board()
        test_board.grid[5].is_covered = False
        self.assertEqual(test_board.check_cell(5).is_covered, 'False')

    def test_is_board_empty(self):
        test_board = board.Board()
        test_board.NUMBER_OF_FREE_TILES = 0
        self.assertEqual(test_board.check_cell(5).is_board_empty, 'True')

    def test_uncover_board_to_first_mine(self):
        test_board = board.Board()
        test_board.grid = [board.Cell('-') for _ in range(settings.ROW_SIZE) for _ in range(settings.COLUMN_SIZE)]

        bombs = 0
        for i in range(settings.NUMBER_OF_TILES):
            if i % 8 == 0 and bombs < settings.NUMBER_OF_BOMBS:
                test_board.grid[i].is_bomb = True
                bombs += 1

        test_board.calculate_adjacent_bombs()
        test_board.uncover_board(36)

        counter = 0
        for i in range(settings.NUMBER_OF_TILES):
            if not test_board.grid[i].is_covered:
                counter += 1

        self.assertEqual(counter, 5)


if __name__ == '__main__':
    unittest.main()
