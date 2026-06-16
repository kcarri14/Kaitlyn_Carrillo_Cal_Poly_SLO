[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/X1hfvLIv)
# Lab 1: Tic Tac Toe Board
Due: 1/8/24

## Overview
In this lab, you will be implementing a basic version of the classic game Tic Tac Toe. You will create a `TicTacToe` class in Python, focusing on understanding data structures and control flow. This lab does not require external libraries such as NumPy.

### Objectives
- Implement a 3x3 Tic Tac Toe board using Python lists.
- Develop a method to check for a winning condition.
- Create a method to randomly fill the board with 'X' and 'O', alternating between them, and then check for a winner.

## Tasks

### Task 1: Initialize the Tic Tac Toe Board
- Implement the `__init__` method in the `TicTacToe` class. This method should be capable of initializing the game board in two ways:
  - If a pre-defined 3x3 board is given upon initialization, use that board.
  - If no board is provided, initialize a new 3x3 board. This board should be a list of lists (3x3) and initially filled with a placeholder (e.g., `None` or an empty string).
- Ensure that the initialization method properly handles both scenarios, creating a versatile and adaptable game setup.

### Task 2: Write a Win Checker Method
- Implement the `check_winner` method in the `TicTacToe` class.
- This method should check all rows, columns, and diagonals for a winning condition (three 'X's or three 'O's in a line).
- The method returns `'X'`, `'O'`, or `None`, indicating the winner or a lack of a winner.

### Task 3: Write a Method to Randomly Assign 'X' or 'O'
- Implement the `randomly_fill_board` method in the `TicTacToe` class.
- The method should fill the board with 'X' and 'O', alternating between them randomly, until the board is full.
- Ensure that each cell is only filled once.
- After the board is full, call the `check_winner` method to determine if there is a winner.
- If there's a winner, print the winner ('X' or 'O'). If it's a tie, print a message indicating a tie.

## Submission
- Submit a single Python file named `tic_tac_toe.py` containing the `TicTacToe` class and the implemented methods.
- Ensure your code is well-commented and follows the best coding practices.

## Grading Criteria
- Correct implementation of the board initialization (Task 1).
- Accurate and efficient checking for a winner (Task 2).
- Proper implementation of the board-filling logic, ensuring randomness and alternating 'X' and 'O' (Task 3).
- Code readability and adherence to coding standards.

Good luck, and have fun with your implementation of Tic Tac Toe!

