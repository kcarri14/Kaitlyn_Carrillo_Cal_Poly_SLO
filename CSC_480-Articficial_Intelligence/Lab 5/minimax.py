#game: connect 4
import numpy as np
import random
import math

row_count = 6
col_count = 7
Player = 1
AI = 2
ai_piece = 'o'
player_piece = 'x'
max_space = 3

def create_board():
    return np.full((row_count, col_count), '', dtype='<U1') 

def is_moves_left(board):
    return np.any(board == '')

def is_valid_location(board, col):
    return board[0][col] == ''

def get_possible_moves(board):
    order = [3, 2, 4, 1, 5, 0, 6]
    return [c for c in order if is_valid_location(board, c)]

def apply_move(board, col, piece):
    new_state = board.copy()
    #print(new_state)
    for r in range(row_count -1, -1, -1):
        #print(r)
        if new_state[r][col] == '':
            new_state[r][col] = piece
            #print(new_state)
            return new_state

def detect_win(board, piece):
    # Horizontal
    for r in range(row_count):
        for c in range(col_count - 3):
            if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3] == piece:
                return True
    # Vertical
    for c in range(col_count):
        for r in range(row_count - 3):
            if board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c] == piece:
                return True
    # Diagonal up-right
    for r in range(row_count - 3):
        for c in range(col_count - 3):
            if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3] == piece:
                return True
    # Diagonal down-right
    for r in range(3, row_count):
        for c in range(col_count - 3):
            if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3] == piece:
                return True
    return False

def evaluate_state(board, player):
    score = 0
    for col in range(2, 5):
        for row in range(row_count):
            if board[row][col] == player:
                if col == 3:
                    score += 3
                else:
                    score+= 2
    # Horizontal pieces
    for col in range(col_count - max_space):
        for row in range(row_count):
            adjacent_pieces = [board[row][col], board[row][col+1], 
                                board[row][col+2], board[row][col+3]] 
            score += evaluate_window(adjacent_pieces, player)
    # Vertical pieces
    for col in range(col_count):
        for row in range(row_count - max_space):
            adjacent_pieces = [board[row][col], board[row+1][col], 
                                board[row+2][col], board[row+3][col]] 
            score += evaluate_window(adjacent_pieces, player)
    # Diagonal upwards pieces
    for col in range(col_count - max_space):
        for row in range(row_count - max_space):
            adjacent_pieces = [board[row][col], board[row+1][col+1], 
                                board[row+2][col+2], board[row+3][col+3]] 
            score += evaluate_window(adjacent_pieces, player)
    # Diagonal downwards pieces
    for col in range(col_count - max_space):
        for row in range(max_space, row_count):
            adjacent_pieces = [board[row][col], board[row-1][col+1], 
                    board[row-2][col+2], board[row-3][col+3]]
            score += evaluate_window(adjacent_pieces, player)
    return score

def evaluate_window(window, piece):
    opp = player_piece if piece == ai_piece else ai_piece
    cnt_p = window.count(piece)
    cnt_o = window.count(opp)
    cnt_e = window.count('')

    score = 0
    # Our threats
    if cnt_p == 4:
        score += 100000
    elif cnt_p == 3 and cnt_e == 1:
        score += 100
    elif cnt_p == 2 and cnt_e == 2:
        score += 10

    if cnt_o == 3 and cnt_e == 1:
        score -= 120
    elif cnt_o == 2 and cnt_e == 2:
        score -= 12

    return score
            
def minimax(state, depth, is_maximizing, ai_piece):
      if depth == 0 or game_over_(state):
          return evaluate_state(state, ai_piece)
      
      if is_maximizing:
          best_score = -float('inf')
          for move in get_possible_moves(state):
              new_state = apply_move(state, move, ai_piece)
              score = minimax(new_state, depth-1, False, ai_piece)
              best_score = max(score, best_score)
          return best_score
      else:
          best_score = float('inf')
          for move in get_possible_moves(state):
              new_state = apply_move(state, move, ai_piece)
              score = minimax(new_state, depth-1, True, ai_piece)
              best_score = min(score, best_score)
          return best_score

def pick_best_move(board, depth, ai_piece):
    #print("inside pick best move")
    curr = ai_piece
    #print("found current player")
    #print(curr)
    ai_turn = (ai_piece == curr)
    #print(ai_turn)
    want_max = (ai_piece == 'o' and ai_turn) or (ai_piece == 'x' and not ai_turn)
    #print(want_max)
    best_move = None
    best_value = -float('inf') if want_max else float('inf')
    #print(best_value)
    for move in get_possible_moves(board):
        #print("inside get possible moves")
        child = apply_move(board, move, ai_piece)
        #print(child)
        score = minimax(child, depth-1, not want_max, ai_piece)
        #print(score)
        if want_max:
            if score > best_value:                
                best_value, best_move = score, move
        else:
            if score < best_value:               
                best_value, best_move = score, move
    return best_move, best_value

def game_over_(board):
    return detect_win(board, ai_piece) or detect_win(board, player_piece) or not is_moves_left(board)

def winner(board):
    if detect_win(board, ai_piece): return ai_piece
    if detect_win(board, player_piece): return player_piece
    return None
      

def main():
    board = create_board()
    turn = random.randint(Player, AI)
    
    #print(board)
    depth = 6
    while not game_over_(board):
        if turn == Player:
            while True:
                col = int(input("Player selected column (0-6): \n"))
                if is_valid_location(board, col):
                    new_board = apply_move(board, col, player_piece)
                    board = new_board
                    turn = AI
                    break
                else:
                    print("Column {col} is full pick another one")
        else:
            #print("inside the else in main")
            move, val = pick_best_move(board, depth, ai_piece)  # not 3
            if move is None:
                #print("No legal moves. Draw.")
                break
            board = apply_move(board, move, ai_piece) 
            print(f"AI drops in column {move} (eval {val}).")
            print(board)
            turn = Player
    w = winner(board)
    print(board)
    if w == 'o':
        print("AI wins! Game over.")
    elif w == 'x':
        print("Player wins! Game over.")
    else:
        print("Draw. Game over.")

                    

if __name__ == "__main__":
    main()
