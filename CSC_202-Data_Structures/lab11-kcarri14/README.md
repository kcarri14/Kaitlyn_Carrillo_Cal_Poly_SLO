[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/qLe-1K5f)
# Lab 11: Priority Queue Game Implementation

## Introduction

In this lab, you will be working on implementing a game using a priority queue, built upon a modified MinHeap class. The MinHeap class will be adapted to manage game players in a priority queue where each player is represented as a tuple `(priority, name, gold)`. Your main objectives will include modifying the MinHeap class to support tuples, implementing game logic that utilizes this priority queue, and ensuring dynamic updates to player priorities and gold based on dice rolls.

## Starter Code

You have been provided with a starter `MinHeap` class that currently supports basic enqueue and dequeue operations. Your task is to enhance this class to work with tuples representing game players and to implement additional functionality required for the game.

## Goals

1. **Modify the MinHeap Class**: Adapt the class to correctly manage tuples, focusing on the `priority` for ordering within the heap.
2. **Implement Game Mechanics**: Use the modified MinHeap to simulate a game where players roll dice to determine their turn order and gain gold.
3. **Dynamic Priority Updates**: Create a method within the MinHeap class to update a player's priority and gold after their turn, based on the outcome of their dice roll.

## Tasks

### Task 1: Modifying the MinHeap Class

- Modify the `enqueue` and `dequeue` methods to correctly handle tuples of the form `(priority, name, gold)`.
- Adjust the `_heapify_up` and `_heapify_down` methods to compare elements based on the `priority` value within the tuple.
- Ensure the class can accurately maintain the heap property for these tuples.

### Task 2: Implementing Game Logic

- Implement an `play one turn` method in the MinHeap class that updates a player's priority (based on a dice roll) and gold. This method should:
    - Get the next player in the heap.
    - Simulate rolling two six-sided dice to determine the new priority and gold increase.
    - Enqueue the player's tuple with the new values and adjust the heap accordingly.


## Requirements

- The MinHeap class must correctly handle tuples, using the first element of each tuple as the priority for heap operations.
- The game should allow players to take turns in an order determined by their priority, with the ability to dynamically change priorities based on dice rolls.


