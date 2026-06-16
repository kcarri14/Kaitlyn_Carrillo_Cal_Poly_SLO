[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/6dXdMh0i)
# Project 4 README: Graph Implementation with Custom Hashtable

This project implements a graph data structure using a custom hashtable for storing adjacency lists. The implementation includes methods for adding edges, performing depth-first search (DFS) traversal, and managing the hashtable used to represent the graph.

## Hashtable Class

The `Hashtable` class provides a custom hashtable implementation designed to store key-value pairs, where each key is a single character representing a vertex, and the value is a list of adjacent vertices (neighbors).

### Methods

#### `__init__(self, capacity=12)`
- Initializes the hashtable with a specified capacity.
- Pseudocode:
  ```
  initialize capacity
  create table with size equal to capacity, filled with None
  set size to 0
  ```

#### `hash(self, key)`
- Computes and returns the hash value for a given key.
- Pseudocode:
  ```
  if key is not a single character:
    raise ValueError
  return ascii value of key character modulo capacity
  ```

#### `insert(self, key, value)`
- Inserts a key-value pair into the hashtable.
- Pseudocode:
  ```
  compute hash for key
  while table at index is not None:
    if key at index matches input key:
      update value at index
      return
    move to next index (with wraparound)
    if back at original index:
      raise exception (table full)
  insert key-value pair at index
  increment size
  ```


#### `insert(self, key, value)`
The `insert` method is crucial for adding key-value pairs to the hashtable, ensuring that data can be efficiently stored and retrieved based on unique keys. This method follows a specific procedure to handle insertion:

1. **Hash Computation**: Initially, it computes the hash of the key to determine the index where the key-value pair should ideally be stored. This computation ensures that data is distributed across the hashtable, reducing the likelihood of collisions.

2. **Collision Handling via Linear Probing**: If the computed index is already occupied, the method employs linear probing to find the next available slot. Linear probing incrementally checks subsequent indices (with wraparound to ensure it stays within the bounds of the table) until an empty slot is found.

3. **Update or Insert**: If the method encounters an index already containing the same key, it updates the existing entry with the new value instead of inserting a duplicate. This ensures data consistency and prevents key duplication within the table.

4. **Full Table Handling**: If the method cycles back to the original index without finding an available slot, it concludes that the hashtable is full and raises an exception, indicating that no more data can be inserted without expanding the table's capacity.

5. **Size Incrementation**: Upon successfully inserting a new key-value pair, the method increments the size attribute of the hashtable, tracking the total number of entries stored.









#### `get(self, key)`
- Retrieves the value associated with a given key.
- Notice our delete function DOES NOT rehash, so we must do a full loop before returning not found
- Pseudocode:
  ```
  compute hash for key
  while True:
    if table at index is None:
      if full loop completed:
        return None
      continue search
    if key at index matches input key:
      return value at index
    move to next index (with wraparound)
    if full loop completed:
      break
  return None
  ```
#### `get(self, key)`
The `get` method retrieves the value associated with a given key, employing the hashtable's structure for rapid access to stored data. This operation involves several steps:

1. **Hash Computation and Initial Search**: Similar to `insert`, it starts by computing the key's hash to find the starting index for the search.

2. **Search with Full Loop Consideration**: The method iterates through the table, accounting for linear probing's effect on data placement. If an index contains `None` (indicating an empty slot), the search continues to the next index, wrapping around the table if necessary.

3. **Key Match Check**: For each non-empty slot encountered, the method checks if the stored key matches the search key. If a match is found, the associated value is returned.

4. **Full Table Traversal**: Given the possibility of gaps due to direct deletion (without rehashing), the method is designed to perform a full loop of the table before concluding that a key is not present. This ensures that all potential slots where the key could be located due to prior linear probing are checked.

#### `delete(self, key)`
- Deletes a key-value pair from the hashtable.
- Notice our delete function DOES NOT rehash, so we must do a full loop before returning not found
- Pseudocode:
  ```
  compute hash for key
  while True:
    if table at index is None:
      if full loop completed:
        return False
      continue search
    if key at index matches input key:
      set table at index to None
      decrement size
      return True
    move to next index (with wraparound)
    if full loop completed:
      break
  return False
  ```
#### `delete(self, key)`
The `delete` function removes a key-value pair from the hashtable, a critical operation for managing and maintaining the dataset stored within the hashtable:

1. **Hash Computation and Search Initiation**: Starting with the hash of the key to determine the initial index, the method looks for the key to delete.

2. **Handling Deletions with Full Loop Search**: The method iterates over the table's indices, considering linear probing's effects on key placement. If it encounters an empty slot (`None`), it continues the search to ensure any keys displaced by probing are still found.

3. **Key Match and Deletion**: Upon finding a match for the key, the method sets the table entry at the index to `None`, effectively deleting the key-value pair from the hashtable.

4. **Size Decrement and Full Loop Completion**: After deletion, the hashtable's size is decremented. Similar to the `get` method, a full loop of the table is performed to ensure the key is not missed due to displacement from linear probing.

5. **Failure to Find Key**: If the method completes a full loop without finding the key, it returns `False`, indicating the key was not present and thus not deleted.

#### `print(self)`
- Prints the contents of the hashtable.
- Pseudocode:
  ```
  print "Hashtable contents:"
  for each index and item in table:
    if item is not None:
      print index, vertex, and neighbors
    else:
      print index is Empty
  ```

## Graph Class

The `Graph` class represents an undirected graph using the custom `Hashtable` for adjacency lists.

### Methods

#### `__init__(self, vertices)`
- Initializes the graph with a specified number of vertices.
- Pseudocode:
  ```
  create a Hashtable with capacity equal to vertices
  ```

#### `add_edge(self, src, dest)`
- Adds an edge between two vertices in the graph.
- Pseudocode:
  ```
  get neighbors of src
  if src has no neighbors:
    insert src with dest as neighbor
  else:
    append dest to src's neighbors
    re-insert src with updated neighbors
  
  get neighbors of dest (repeat the above steps for dest and src)
  ```

### Detailed Explanation for `add_edge` Function

The `add_edge` function is a fundamental component of the `Graph` class, designed to establish connections between vertices in an undirected graph. This method meticulously updates the adjacency list to reflect the bidirectional relationship between the source (`src`) and destination (`dest`) vertices, ensuring the graph accurately represents the links between nodes.

Upon invocation with a pair of vertices, the `add_edge` function performs the following operations:

1. **Check for Existing Adjacency List**: For each vertex in the pair, the function checks whether an adjacency list already exists within the hashtable. The adjacency list is a collection of neighbor vertices to which the vertex is directly connected.
   
2. **Update or Create Adjacency List**:
   - If the adjacency list for the vertex does not exist, the function creates a new list containing the counterpart vertex and inserts it into the hashtable.
   - If the adjacency list already exists, the function appends the counterpart vertex to the existing list, ensuring the connection is recorded.

3. **Ensure Bidirectional Connection**: The function applies the above steps to both vertices in the pair. This ensures the graph remains undirected, with each edge accurately representing a two-way link. For instance, adding an edge between `A` and `B` will make `B` accessible from `A` and vice versa.

4. **Graph Integrity Maintenance**: By updating the adjacency lists for both involved vertices, the `add_edge` function maintains the structural integrity of the graph. This integrity is crucial for accurately performing graph operations, such as traversal, pathfinding, and cycle detection.


#### `dfs_traversal(self, start_vertex)`
- **Description**: Performs a depth-first search (DFS) traversal starting from a given vertex. This method integrates the traversal logic into a single function, managing visited vertices and recursion within itself.
- **Pseudocode**:
  ```
  FUNCTION dfs_traversal(start_vertex):
    IF visited set is not defined:
      CREATE a set for visited vertices
    ADD start_vertex to visited
    PRINT start_vertex
    FOR each neighbor in the adjacency list of start_vertex:
      IF neighbor is not visited:
        RECURSIVELY call dfs_traversal with neighbor
  ```

### Detailed Explanation

The `dfs_traversal` method is designed to perform a depth-first search from a specified starting vertex. It leverages recursion to explore as far as possible along each branch before backtracking. This method is self-contained, handling the maintenance of a set of visited vertices to ensure each vertex is visited exactly once during the traversal. The method's initial call begins with the `start_vertex`, and as it progresses, it recursively explores each unvisited neighbor.

This approach to DFS traversal is straightforward yet powerful, allowing for the exploration of all vertices connected to the starting point. It's particularly useful in applications like finding connected components, checking for cycles, and solving puzzles and games that can be modeled as graphs.


Certainly! Here's an addition to the README that outlines specific tasks related to implementing the `Hashtable` and `Graph` classes, focusing on the key methods: `insert`, `get`, `delete` for the hashtable, and `add_edge`, `dfs_traversal` for the graph.

---

## Tasks

This section outlines specific tasks for implementing and utilizing the `Hashtable` and `Graph` classes. These tasks are designed to ensure a comprehensive understanding and application of data structure and algorithm concepts in a practical setting.

### Hashtable Implementation Tasks

1. **Implement the `insert` Method**
   - Task: Implement the `insert` function in the `Hashtable` class to add key-value pairs. Handle collisions using linear probing.
   - Goal: Ensure the method efficiently stores data, even in the event of hash collisions.

2. **Implement the `get` Method**
   - Task: Develop the `get` function to retrieve values based on their keys. Account for linear probing when searching for keys.
   - Goal: Achieve fast retrieval of values, correctly navigating through the linear probing sequence.

3. **Implement the `delete` Method**
   - Task: Create the `delete` function to remove key-value pairs from the hashtable. Ensure a full loop is performed before declaring a key not found.
   - Goal: Correctly remove entries and maintain the integrity of the hashtable's structure and size.

### Graph Implementation Tasks

1. **Implement the `add_edge` Method**
   - Task: Implement the `add_edge` method in the `Graph` class to create undirected edges between vertices. Use the hashtable for storing adjacency lists.
   - Goal: Accurately represent the graph's connections, ensuring bidirectional consistency between vertices.

2. **Implement the `dfs_traversal` Method**
   - Task: Develop the `dfs_traversal` method to perform a depth-first search starting from a given vertex. Use recursion to explore the graph.
   - Goal: Efficiently traverse the entire graph, visiting each vertex once, and demonstrate the application of DFS in graph exploration and analysis.



### No Need to Submit your own tests
- Focus on getting ready for finals