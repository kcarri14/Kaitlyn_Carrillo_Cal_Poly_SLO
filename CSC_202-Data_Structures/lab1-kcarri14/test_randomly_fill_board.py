import unittest
from tic_tac_toe import TicTacToe

class TestTicTacToeRandomlyFillBoard(unittest.TestCase):
    def test_random_fill(self):
        game = TicTacToe()
        game.randomly_fill_board()
        
        # Test the board is full
        for row in game.board:
            self.assertTrue(all(cell in ['X', 'O'] for cell in row))
    
        # Test that the difference in counts between X and O is at most 1
        flat_board = sum(game.board, [])
        self.assertIn(abs(flat_board.count('X') - flat_board.count('O')), [0, 1])


    def test_random_fill_and_check_winner(self):
        game = TicTacToe()
        game.randomly_fill_board()
        # Since the result is random, we only check if the winner is valid
        winner = game.check_winner()
        self.assertIn(winner, ['X', 'O', None])

if __name__ == '__main__':
    unittest.main()
