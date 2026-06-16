import unittest
from tic_tac_toe import TicTacToe

class TestTicTacToeCheckWinner(unittest.TestCase):
    def test_winner_in_row(self):
        game = TicTacToe([['X', 'X', 'X'], [None, 'O', None], ['O', None, None]])
        self.assertEqual(game.check_winner(), 'X')

    def test_winner_in_column(self):
        game = TicTacToe([['O', None, 'X'], ['O', 'X', None], ['O', None, None]])
        self.assertEqual(game.check_winner(), 'O')

    def test_winner_in_diagonal(self):
        game = TicTacToe([['X', None, 'O'], [None, 'X', None], ['O', None, 'X']])
        self.assertEqual(game.check_winner(), 'X')

    def test_no_winner(self):
        game = TicTacToe([['X', 'O', 'X'], ['X', 'O', 'O'], ['O', 'X', 'O']])
        self.assertIsNone(game.check_winner())

if __name__ == '__main__':
    unittest.main()
