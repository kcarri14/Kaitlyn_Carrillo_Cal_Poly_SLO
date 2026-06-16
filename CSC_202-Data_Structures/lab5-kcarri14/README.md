[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/R23IFq-V)
# Lab 5: Implementing Dunder Methods in a Doubly Linked List

## Overview

In this lab, we will delve into the implementation of a Doubly Linked List (DLL) in Python, focusing on incorporating several 'dunder' (double underscore) methods. These special methods allow us to define how our custom objects behave with built-in Python operations. Understanding and implementing these methods is key to creating more intuitive and Pythonic classes.

## Introduction to Dunder Methods

Dunder methods, also known as magic or special methods, are a set of predefined methods in Python that you can override in your classes. They are identified by their double underscores at the beginning and end, e.g., `__init__`, `__str__`. These methods allow your objects to interact with built-in Python functions or operators. For example, `__str__` is used to determine the string representation of an object, and `__eq__` is used to define object equality.


### Lab Tasks


### Task 1: Implement `__eq__` Method

**Objective:** Compare two Doubly Linked Lists (DLLs) for equality.

**Guidance:**
1. Start by comparing the lengths of the two lists. If they are different, they can't be equal.
2. If the lengths are the same, iterate through both lists simultaneously, comparing the data in each node.
3. If all corresponding nodes are equal, return `True`. Otherwise, return `False`.



### Task 2: Implement `__getitem__` Method

**Objective:** Retrieve an element from the DLL using its index.

**Guidance:**
1. Validate the index: it should be an integer and within the valid range.
2. Traverse the list until you reach the desired index.
3. Return the data of the node at that index.



### Task 3: Implement `__setitem__` Method

**Objective:** Assign a new value to an element in the DLL using its index.


### Task 4: Writing Test Cases
For Task 4, you will write test cases for each of the previously implemented methods (`__eq__`, `__getitem__`, and `__setitem__`) to ensure they function as expected.

Create a file named `test_student.py` and implement the following test cases using Python's `unittest` framework:

**1. Test for `__eq__` Method:**
- Test if two lists with the same elements are equal.
- Test if two lists with different elements are not equal.

**2. Test for `__getitem__` Method:**
- Test retrieving elements at various indexes.
- Test index out of range scenario.

**3. Test for `__setitem__` Method:**
- Test setting elements at various indexes.
- Test index out of range scenario.



**Guidance:**
1. Similar to `__getitem__`, first validate the index.
2. Traverse the list to find the node at the specified index.
3. Update the `data` attribute of this node.



### Additional Tips:
- Consider edge cases, like when the list is empty or if the index is exactly at the end of the list.
- For `__eq__`, you might also need to handle the case where `other` is not a `DoublyLinkedList`.
- Remember to adhere to Python's conventions and best practices for readability and maintainability.


