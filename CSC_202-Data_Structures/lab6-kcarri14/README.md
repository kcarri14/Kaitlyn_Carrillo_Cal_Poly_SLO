[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/rwcQ3ZBD)
# Lab 5: Stack Operations and Card Stack Processing - A Two-Day Lab

## Overview
Lab 5 is a two-day lab focused on understanding and implementing stack operations using Python's `array` module. This lab includes building a custom stack class, reversing a stack, simulating a card sorting game, and writing unit tests.

## Day 1: Stack Implementation and Basic Operations

### ArrayStack Class
Participants will create the `ArrayStack` class, a custom stack implementation using Python's `array.array`.

#### Features
- `push(item)`: Adds an item to the stack, with overflow checks.
- `pop()`: Removes and returns the top item, with underflow checks.
- `peek()`: Retrieves the top item without removing it.
- `is_empty()`: Checks if the stack is empty.
- `is_full()`: Checks if the stack is at full capacity.
- `size()`: Returns the number of items in the stack.

#### Task 1: Implement Push and Pop
Implement `push` and `pop` methods in `ArrayStack`, handling overflow and underflow using `is_empty` and `is_full`.

## Day 2: Advanced Stack Operations and Card Sorting Game

### Task 2: Reversing a Stack
Create a function `reverse_stack` that uses a temporary stack to reverse the order of elements in a given stack.


### Task 3: Card Stack Sorting Game Simulation

#### Objective
The objective of Task 3 is to develop a function, `process_card_stack`, that simulates a card sorting game. In this game, you are provided with a stack of cards numbered from 1 to 13 in a randomized order. The goal is to sort these cards into a separate "solution" stack in ascending order, following specific rules and procedures.

#### Functionality
- **Input**: A stack of unique cards numbered from 1 to 13 in random order.
- **Output**: A sorted "solution" stack with cards arranged from 1 (bottom) to 13 (top).

#### Game Rules
1. **Single Card Processing**: Process the cards by popping one card at a time from the input stack.
2. **Orderly Placement**: If the popped card is the next in ascending sequence for the solution stack, place it on the solution stack. For example, if the solution stack's top card is 3, you can place 4 next.
3. **Discard Stack Usage**: If the card cannot be placed on the solution stack (not in sequence), push it onto a separate "discard" stack.
4. **Recycling Discard Stack**: Once the input stack is empty, reverse the discard stack and transfer its cards back to the input stack.
5. **Repeating the Process**: Continue processing until either the solution stack is correctly sorted, or it's determined that the game cannot be solved with the given order of cards.
6. **Error Checking**: The function should handle error scenarios such as receiving a `None` input, a non-stack input, or a stack of incorrect size (not 13).

#### Game End Conditions
- **Successful Sorting**: The game is successfully solved if all cards are sorted into the solution stack in ascending order from 1 to 13.
- **Unsolvable Game**: The game is deemed unsolvable if, after several cycles of processing, the cards cannot be arranged in the required order.


### Example Usage
An example demonstrates shuffling a card stack, processing it, and printing the sorted result.

## Task 4: Writing Unit Tests in `test_student.py`
Write your unit tests in `test_student.py`, focusing on:
- At least two test cases for each function (`push`, `pop`, `reverse_stack`, and `process_card_stack`).
- Include tests for edge cases and error handling scenarios.

## Requirements
- Complete the `ArrayStack` class and the specified tasks.
- Write comprehensive unit tests in `test_student.py`.

## Testing
- Ensure the correct functionality of all methods in `ArrayStack`.
- Validate the behavior of `reverse_stack` and `process_card_stack` through unit tests.

