[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/-dQVkaKV)
# Project 1: Polynomial Calculator Using Singly Linked Lists

## Overview
In Project 1 for CS 202: Data Structures, you will develop a `Calculator` class to manipulate polynomials represented as singly linked lists. Each node in these lists holds a polynomial term, where `node.val` is the coefficient, and its position indicates the term's degree. For example, a polynomial \( 5x^2 + 3x + 2 \) is represented as `5 -> 3 -> 2`, and \( 2x + 7 \) as `2 -> 7`, while \( 8 \) is simply `8`.

### Methods to Implement

1. **Addition**:
    - **Input**: Given the head nodes of two singly linked lists representing polynomials.
    - **Operation**: Add the polynomials term by term, considering polynomials of differing lengths.
    - **Examples**: 
        - Example 1:
          - Polynomial 1: \( 3x^2 + 0x + 5 \) (List: `3 -> 0 -> 5`)
          - Polynomial 2: \( 5x^2 + 2x + 1 \) (List: `5 -> 2 -> 1`)
          - Result: \( 8x^2 + 2x + 6 \)
        - Example 2:
          - Polynomial 1: \( 4x^3 + 3x \) (List: `4 -> 0 -> 3 -> 0`)
          - Polynomial 2: \( 2x + 1 \) (List: `2 -> 1`)
          - Result: \( 4x^3 + 2x^2 + 5x + 1 \)

2. **Subtraction**:
    - **Input**: Given the head nodes of two singly linked lists representing polynomials.
    - **Operation**: Subtract the second polynomial from the first, term by term, accounting for different lengths.
    - **Examples**:
        - Example 1:
          - Polynomial 1: \( 6x^3 + 4x^2 + 0x + 2 \) (List: `6 -> 4 -> 0 -> 2`)
          - Polynomial 2: \( 1x^3 + 2x^2 + 3x + 4 \) (List: `1 -> 2 -> 3 -> 4`)
          - Result: \( 5x^3 + 2x^2 - 3x - 2 \)
        - Example 2:
          - Polynomial 1: \( 7x + 3 \) (List: `7 -> 3`)
          - Polynomial 2: \( 2x^2 + 4x + 1 \) (List: `2 -> 4 -> 1`)
          - Result: \( -2x^2 + 3x + 2 \)

3. **Differentiation**:
    - **Input**: Given the head of a singly linked list representing a polynomial.
    - **Operation**: Differentiate the polynomial.
    - **Output**: A new linked list representing the differentiated polynomial.
    - **Resource**: A tutorial on polynomial differentiation can be found at: **https://www.youtube.com/watch?v=-CTaxKTzbEI**
    - **Examples**:
        - Example 1:
          - Polynomial: \( 7x^4 + 0x^3 + 3x^2 + 0x + 1 \) (List: `7 -> 0 -> 3 -> 0 -> 1`)
          - Result: \( 28x^3 + 0x^2 + 6x + 0 \) (List: `28 -> 0 -> 6 -> 0`)
        - Example 2:
          - Polynomial: \( 5x^3 + 4x^2 \) (List: `5 -> 4 -> 0`)
          - Result: \( 15x^2 + 8x \) (List: `15 -> 8`)

4. **Anti-Derivative AKA Indefinite Integral**:
    - **Input**: Given the head of a singly linked list representing a polynomial.
    - **Operation**: Compute the anti-derivative of the polynomial.
    - **Output**: A new linked list representing the anti-derivative.
    - **Resource**: A tutorial on polynomial anti-derivatives can be found at **https://www.youtube.com/watch?v=Jd8lurQhyNM**
    - **Examples**:
        - Example 1:
          - Polynomial: \( 4x^3 + 3x^2 + 2x + 1 \) (List: `4 -> 3 -> 2 -> 1`)
          - Result: \( x^4 + x^3 + x^2 + x \)  (List: `1 -> 1 -> 1 -> 1`)

        - Example 2:
          - Polynomial: \( 6x^2 + 5x \) (List: `6 -> 5 -> 0`)
          - Result: \( 2x^3 + \frac{5}{2}x^2 \) (List: `2 -> 2.5`)

### Requirements

- **Robustness**: Your methods should be robust, handling edge cases and raising appropriate errors:
    - Non-numeric coefficients should trigger a `TypeError`.
    - Empty (`None`) input should trigger a `ValueError`.
    - Ensure all middle terms are present, using zero coefficients if necessary. Pay special attention to polynomials of differing lengths.

- **Documentation**: Provide clear docstrings for each method, explaining the inputs, process, and outputs. 

- **Comments**: Include comments for any steps that can look confusing

- **Testing**: Include multiple test cases demonstrating the functionality of each method, especially edge cases.

- **Resources**: Links to tutorials on polynomial differentiation and anti-differentiation will be provided to assist you.

### Submission

Your final submission should include:

1. The `Calculator` class with all four methods implemented in `proj1.py`.
2. A set of test cases for each method in `test_student.py`.
3. Docstrings for each method of your implementation.
4. Submit your project via GitHub Classroom.


### Grading

80% of the score will be the result of passing my test cases. 
20% will be a manual review of documentation and your submitted test cases

This project will deepen your understanding of linked lists, polynomial operations, and the application of data structures in problem-solving. Good luck!