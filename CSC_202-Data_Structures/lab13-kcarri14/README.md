[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/IBPDGKRz)
# Lab 13: Exploring Hash Tables

## Overview
In Lab 13, we dive into the world of hash tables, exploring their implementation, usage, and the underlying algorithms that make them efficient for data storage and retrieval. This lab consists of six tasks, each designed to enhance your understanding of hash tables, from basic operations like insertion and search to more complex functionalities such as resizing and handling collisions.

### Objectives
- Implement a hash table using separate chaining
- Explore hashing functions and their impact on data distribution within a hash table
- Understand and implement hash table resizing based on load factor
- Practice inserting, searching, and deleting key-value pairs in a hash table


## Task 1: Initialize the Hash Table

**Goal:** Set up a basic hash table structure.

**Steps:**
1. Define a class `HashTable` with an `__init__` method.
2. In the `__init__` method, initialize the following properties:
   - `capacity`: Set this to the initial capacity of the hash table.
   - `table`: This should be a list of empty lists (buckets) with a length equal to the capacity. Each bucket will use separate chaining to handle collisions.
   - `size`: Track the current number of key-value pairs in the hash table. Initialize this to `0`.

## Task 2: Implement the Hash Function

**Goal:** Create a simple hash function to map keys to indices in the hash table.

**Steps:**
1. Within the `HashTable` class, define a method `simple_hash` that takes a `key` as its argument.
2. Convert the `key` to a string (if it isn't already) to ensure consistency.
3. Calculate the hash index by summing the ASCII values of the characters in the key, then taking the modulus of this sum with the table's capacity.
4. Return the calculated index.

## Task 3: Insert Key-Value Pairs

**Goal:** Enable insertion of key-value pairs into the hash table.

**Steps:**
1. Define an `insert` method in the `HashTable` class that accepts `key` and `value` parameters.
2. Use the `simple_hash` method to determine the index for the given key.
3. Check if the key already exists in the corresponding bucket:
   - If it does, update the value.
   - If not, append a new tuple `(key, value)` to the bucket.
4. Increment the `size` of the hash table.
5. After insertion, call `check_load_factor` to ensure the load factor is within acceptable limits.

## Task 4: Search for Key-Value Pairs

**Goal:** Implement functionality to search for a value by its key.

**Steps:**
1. Define a `search` method in the `HashTable` class that takes a `key` as its argument.
2. Calculate the index for the key using the `simple_hash` method.
3. Iterate over each key-value pair in the corresponding bucket:
   - If the key is found, return its value.
   - If the key is not found by the end of the bucket, return `None`.

## Task 5: Delete Key-Value Pairs

**Goal:** Allow deletion of key-value pairs from the hash table.

**Steps:**
1. Define a `delete` method in the `HashTable` class with a `key` parameter.
2. Find the bucket for the key using `simple_hash`.
3. Iterate over the bucket and locate the key-value pair to delete:
   - Remove the key-value pair from the bucket.
   - Decrement `size`.
   - Return `True` to indicate successful deletion.
4. If the key is not found, return `False`.

## Task 6: Handle Load Factor and Resize

**Goal:** Ensure the hash table maintains efficiency by resizing based on the load factor.

**Steps:**
1. Define a `check_load_factor` method to evaluate if resizing is needed:
   - Calculate the load factor as `size / capacity`.
   - If the load factor exceeds `0.75`, call the `resize` method with double the current capacity.
2. Implement the `resize` method:
   - Create a new, larger table and rehash all existing key-value pairs into this new table.
   - Update the `capacity` and reset `size` as you re-insert elements.
3. In `insert`, ensure `check_load_factor` is called after adding a new key-value pair to possibly trigger resizing.
