[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/7UvHFtEq)
# Lab 10: Understanding and Implementing Heaps and HeapSort

## Introduction

This lab is designed to deepen your understanding of heap data structures and their applications, specifically in sorting algorithms. Heaps are a category of tree-based data structures that satisfy heap properties. In this lab, you will first modify a provided Max Heap implementation to create a Min Heap and then use your Min Heap to implement the HeapSort algorithm, sorting an unsorted list in ascending order.

## Part 1: From Max Heap to Min Heap

### Objective

Modify the provided Max Heap code to implement a Min Heap. This involves understanding the differences between Max Heaps and Min Heaps and adjusting the heap property checks and operations accordingly.

### Starting Code

You are provided with a Max Heap implementation in Python. Your task is to modify this code to reflect a Min Heap's behavior, focusing on the `heapify_up`, `heapify_down`, `insert`, `peek`, and `extract_max` methods.

### Tasks for Part 1

1. **Modify `heapify_up` and `heapify_down` Methods:** Adjust these methods to ensure the parent node is always less than or equal to its children, maintaining the Min Heap property.
2. **Update the `insert` Method:** Ensure that new elements maintain the Min Heap property when added.
3. **Adjust `extract_max` Method:** Rename to `extract_min` and modify it to remove and return the smallest element in the heap.
4. **Test Your Implementation:** Adjust the example usage provided to test your Min Heap, inserting elements and extracting the minimum element to demonstrate correct heap operations.

## Part 2: Implementing HeapSort Using Min Heap

### Objective

Use your Min Heap implementation from Part 1 to perform HeapSort on an unsorted list, sorting it in ascending order.

### Tasks for Part 2

1. **Implement HeapSort Function:** Create a function that takes an unsorted list, builds a Min Heap, and uses it to sort the list in ascending order by repeatedly extracting the minimum element.
2. **Utilize Your Min Heap:** Use the Min Heap class from Part 1 for the heap operations required by HeapSort.
3. **Test Your HeapSort Implementation:** Provide unsorted lists to your HeapSort function, and demonstrate its correctness by printing the original and sorted lists.

