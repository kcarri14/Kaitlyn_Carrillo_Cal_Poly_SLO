[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/QqsZdLq4)
# Lab 2: Recursion

## Overview
In this lab, you will be implementing and testing three different functions in Python. These functions will involve concepts like iteration, recursion, and binary search. Additionally, you will write your own test cases to validate the functionality of your code.

## Tasks
You are required to complete the following tasks in the `lab2.py` file:

### Task 1: Iterative Maximum Finder
- **Function Name:** `max_list_iter`
- **Description:** This function finds the maximum value in a list of integers using iteration.
- **Parameters:**
  - `int_list` - A list of integers.
- **Returns:** The maximum integer in the list. If `int_list` is empty, returns `None`. If `int_list` is `None`, raises `ValueError`.

### Task 2: Recursive List Reversal
- **Function Name:** `reverse_rec`
- **Description:** This function recursively reverses a list of integers.
- **Parameters:**
  - `int_list` - A list of integers.
- **Returns:** A list containing the elements of `int_list` in reverse order. If `int_list` is `None`, raises `ValueError`.

### Task 3: Recursive Binary Search
- **Function Name:** `bin_search`
- **Description:** This function searches for a target value within a specified range of a list of integers using recursion.
- **Parameters:**
  - `target` - The value to search for.
  - `low` - The lower index of the range.
  - `high` - The upper index of the range.
  - `int_list` - A list of integers.
- **Returns:** The index of `target` in `int_list` if found within `int_list[low..high]`. If not found, returns `None`. If `int_list` is `None`, raises `ValueError`.

## Additional Task: Writing Test Cases
- **File:** `test_student.py`
- **Requirement:** For each of the above functions, write your own test cases to validate their functionality. Ensure your tests cover various scenarios including edge cases.

## Submission Guidelines
- Complete the tasks in the `lab2.py` file.
- Write your test cases in the `test_student.py` file.
- Make sure your code adheres to the provided specifications for each function.
- Submit your `lab2.py` and `test_student.py` files via github by the specified deadline.

PS. you can run the tests locally via these terminal commands
python -m unittest test_max.py
python -m unittest test_reverse.py
python -m unittest test_search.py


