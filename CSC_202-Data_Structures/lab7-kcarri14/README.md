[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/c7pruwE3)
# Lab 7: Queue Sorting with Linked Lists

## Overview
Lab 7 focuses on implementing and testing a linked list queue in Python. The primary objectives are to understand queue operations using linked lists, write test cases, and analyze the time complexity of the provided sorting solution.

### Task 1: Complete the Implementation Details for Enqueue and Dequeue

You are required to implement the `enqueue` and `dequeue` methods of the `LinkedListQueue` class. This class represents a queue using a singly linked list. Each node in the linked list is an instance of the `Node` class.

**Node Class:**
```python
class Node:
    """A Node in a linked list."""
    def __init__(self, value):
        self.value = value
        self.next = None
```

**LinkedListQueue Class:**
```python
class LinkedListQueue:
    """A Queue implementation using a linked list."""
    ...
    def enqueue(self, value):
        """Add an item to the rear of the queue."""
        # Implementation here

    def dequeue(self):
        """Remove an item from the front of the queue."""
        # Implementation here

    # Other methods...
```

### Task 2: Write Test Cases for the Solution Queue Function in Task 3

In `test_student.py`, write test cases for the `sort_linked_list_queue_correctly` function. Ensure that your test cases cover various scenarios, including edge cases. Each test case should have a comment explaining its purpose.

### Task 3: Complete the Get Solution Queue

The `sort_linked_list_queue_correctly` function sorts a linked list queue from high to low in a solution queue. As you dequeue from the queue check if it can be enqueued to the solutiuon queue, else enqueue it back to the original queue. Your task is to complete this function following the specified method.

**Function Implementation:**
```python
def sort_linked_list_queue_correctly(queue):
    """
    Sorts a linked list queue from high to low using the specified method.
    # Complete the documentation...
    """
    # Function implementation...
```


### Task 4: Analyze the Time Complexity of Your Solution

For this task, there is no submission required. Analyze the time complexity of the `sort_linked_list_queue_correctly` function. Consider the best, worst, and average case scenarios in your analysis.

