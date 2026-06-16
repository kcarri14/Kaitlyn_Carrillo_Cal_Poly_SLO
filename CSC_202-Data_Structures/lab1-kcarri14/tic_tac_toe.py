import random



class TicTacToe:
    def __init__(self, board=None):
        if board:
            if len(board) != 3:
                raise ValueError
            self.board = board
        else:
            self.board = [[None for _ in range(3)]for _ in range(3)]     

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]: #Checks for a row win
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i]: #Checks for a colmun win
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2]: #Checks diagonals
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0]: #Checks Diagonals
            return self.board[0][2]
        
        return None

    
    def randomly_fill_board(self):
        avail_spots = [(i, j) for i in range(3) for j in range(3)]
        random.shuffle(avail_spots)
        symbols = ['X', 'O']
        turn = 0

        for i, j in avail_spots:
            if self.board[i][j] is None:
                self.board[i][j] = symbols[turn % 2]
                turn += 1

        count_board = sum(self.board, [])
        x_count = count_board.count('X')
        o_count = count_board.count('O')
        difference = abs(x_count - o_count)


        winner = self.check_winner()

        if difference <= 1 and x_count + o_count == 9:

            if winner == "X":
               return "Winner is X"
            elif winner == "O":
                return "Winner is O"
            else:
               return "Game is a Tie"
        return None       
    



TicTacToe()



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
