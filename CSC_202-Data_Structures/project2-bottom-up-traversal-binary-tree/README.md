[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/DmyoIUUE)
# Project 2: Bottom-Up Level Order Traversal of a Binary Tree

## Overview

In this project, you will develop a function to perform a bottom-up, level-by-level traversal of a binary tree. Unlike traditional level-order traversal which processes the tree from the top down, this approach requires you to collect node values at each level from the bottom up.

## Objectives

- Apply Breadth-First Search (BFS) traversal to navigate through the tree level by level.
- Use a stack to invert the order of tree levels collected via BFS, achieving a traversal that presents node values from the bottom level up.

## Requirements

- Proficiency in Python 3.x.
- Understanding of binary trees and their traversal algorithms.
- Familiarity with the concepts of queues and stacks, and their implementation as linked lists.

## Custom Data Structures

### LinkedListQueue

- A queue data structure, implemented as a linked list, will hold nodes yet to be processed in the BFS traversal.
- Key methods to implement: `enqueue(item)`, `dequeue()`, and `isEmpty()`.

### LinkedListStack

- A stack data structure, also implemented as a linked list, will be used to reverse the order of tree levels.
- Key methods to implement: `push(item)`, `pop()`, and `isEmpty()`.

## Required Steps

1. **Bottom-Up BFS Function (`bottomUpBFS`)**:
    - Initialize the BFS queue with the root node.
    - Traverse the tree using BFS, processing nodes level by level.
    - Push node values or entire levels onto a stack to reverse their order.
    - After traversal, transfer items from the stack to a final queue or another structure that maintains the bottom-up order for presentation or further processing.

2. **Student Made Unittests**:
    - Write 4 Unittests for your bottomUpDFS function
    - Write them in test_student.py

## Tips and Guidance

- **Start Simple**: Ensure basic functionality of your `LinkedListQueue` and `LinkedListStack` before tackling the tree traversal logic.
- **Understand BFS**: A clear grasp of BFS is crucial. Practice with simpler examples if necessary.
- **Debug Incrementally**: Test each component individually. Use print statements or debugging tools to verify the queue and stack operations, as well as the BFS process.
- **Visualize the Tree**: Drawing the tree and manually tracing the traversal can offer insights into how your code should operate, especially for understanding how the bottom-up reversal works.
- **Consider Edge Cases**: Include tests for various tree configurations, including empty trees, trees with a single node, and imbalanced trees.

## Expected Outcome

Completing this project will enhance your understanding of tree traversal algorithms, specifically BFS, and give you practical experience with implementing and manipulating advanced data structures like linked lists in the form of queues and stacks. This project not only solidifies foundational computer science concepts but also prepares you for solving complex problems involving data structure manipulation and algorithm design.