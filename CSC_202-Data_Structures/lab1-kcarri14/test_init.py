import unittest
from tic_tac_toe import TicTacToe

class TestTicTacToeInit(unittest.TestCase):
    def test_empty_board_initialization(self):
        game = TicTacToe()
        expected_board = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(game.board, expected_board)

    def test_predefined_board_initialization(self):
        predefined_board = [['X', 'O', 'X'], ['O', None, 'X'], [None, 'O', None]]
        game = TicTacToe(predefined_board)
        self.assertEqual(game.board, predefined_board)

    def test_board_size_on_initialization(self):
        game = TicTacToe()
        self.assertEqual(len(game.board), 3)
        for row in game.board:
            self.assertEqual(len(row), 3)

    def test_invalid_board_initialization(self):
        invalid_board = [['X', 'O'], ['O', 'X']]
        with self.assertRaises(ValueError):
            TicTacToe(invalid_board)

if __name__ == '__main__':
    unittest.main()
