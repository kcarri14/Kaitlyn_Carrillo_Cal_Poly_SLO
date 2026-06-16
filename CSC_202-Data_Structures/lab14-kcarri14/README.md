[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/iST9HkJ_)
# Lab 14: Graph Theory in Python - Detailed Overview


## Task 1: Representing Graphs

Graph representation is crucial for solving problems related to networks, relationships, and paths. This task introduces two primary ways to represent graphs: adjacency matrices and adjacency lists.

### Define Adjacency Matrices
- **Adjacency Matrix for Graph1**:
  - Construct an adjacency matrix where each row and column represent vertices.
  - A cell (i, j) with value 1 indicates a direct edge from vertex i to j, and 0 indicates no direct edge.
  - This matrix representation is useful for dense graphs and when edge existence checks are frequent.

- **Adjacency Matrix for Graph2**:
  - Similar to Graph1, create an adjacency matrix based on the structure of Graph2.
  - This exercise helps understand how different graph structures are represented in a matrix form.

## Task 2: Converting to Adjacency Lists

Adjacency lists offer a more space-efficient way to represent graphs, especially sparse ones. This task involves converting the adjacency matrices of Graph1 and Graph2 into adjacency lists.

### Conversion to Adjacency Lists
- **Adjacency List for Graph1**:
  - Convert the adjacency matrix into a list where each vertex has a list of directly connected vertices.
  - This method is preferred for sparse graphs or when iterating over neighbors of a given vertex.

- **Adjacency List for Graph2**:
  - Apply the same conversion process to Graph2.
  - Understand the advantages of adjacency lists in terms of space efficiency and traversal speed.

## Task 3: Breadth-First Search (BFS)

BFS is a fundamental graph traversal algorithm that explores the graph layer-wise. This task demonstrates how to implement BFS using adjacency lists.

### Implement BFS
- **BFS Implementation**:
  - Start from a given node and visit all its neighbors before moving to the nodes at the next level.
  - Keep track of visited nodes to avoid revisiting and use a queue to manage the order of exploration.
  - Return the order of nodes visited. This is useful for understanding the structure of the graph and for algorithms that need to process nodes in a specific order.

# Details

- **Initialize Data Structures**:
  - **`visited` Set**: Initializes an empty set to keep track of visited vertices, ensuring each vertex is processed only once.
  - **`queue`**: Initializes a queue with the `start_vertex` as its first element. This queue will manage the order in which vertices are visited.
  - **`bfs_order` List**: Initializes an empty list to record the order in which vertices are visited during the BFS traversal.

- **Traversal Process**:
  - Begins a loop that continues as long as there are vertices in the `queue` to be processed.
  - **Dequeue Operation**: Removes and returns a vertex from the front of the queue, assigning it to `current_vertex`.
  - **Check for Visited Status**:
    - If `current_vertex` has not been visited (not in `visited` set), it proceeds with the following steps:
      - **Record Visitation**: Appends `current_vertex` to the `bfs_order` list to track the visitation order.
      - **Mark as Visited**: Adds `current_vertex` to the `visited` set to prevent re-visitation.
      - **Queue Neighbors**: Iterates over all neighbors of `current_vertex` (as listed in the `adjacency_list`). For each neighbor not already visited, it adds the neighbor to the `queue`. This step ensures that all directly connected vertices are queued for visitation in a breadth-first manner.

- **Return BFS Order**:
  - Once the queue is empty, indicating that there are no more vertices to visit, the function returns the `bfs_order` list. This list reflects the order in which vertices were visited during the BFS traversal.


## Task 4: Topological Sorting

Topological sorting is crucial for directed acyclic graphs (DAGs), where you need to order vertices linearly based on dependencies.

### Topological Sorting on Directed Graph
- **Implement Topological Sort**:
  - Use depth-first search (DFS) to explore the graph and sort the vertices such that for every directed edge u → v, u precedes v in the order.
  - This sorting is vital in scenarios like scheduling tasks, resolving dependencies, and more.

# Details
- **Define `topological_sort_util` Function**:
  - **Purpose**: A helper function used by `topological_sort` to perform depth-first search (DFS) recursively.
  - **Parameters**:
    - `node`: The current node being visited.
    - `visited`: A set that tracks which nodes have been visited to avoid cycles.
    - `stack`: A list that acts as a stack to keep track of the nodes in their order of processing.
    - `adjacency_list`: The graph represented as an adjacency list.
  - **Process**:
    - Mark the current `node` as visited by adding it to the `visited` set.
    - Check if the current `node` has outgoing edges by verifying its presence in the `adjacency_list`.
    - For each neighbor of the current `node` that has not been visited, recursively call `topological_sort_util` with the neighbor.
    - After visiting all neighbors, append the current `node` to the `stack`. This step occurs post-recursion to ensure that all dependents of the node are processed first.

- **Define `topological_sort` Function**:
  - **Purpose**: Performs topological sorting on the given directed graph.
  - **Parameters**:
    - `adjacency_list`: The graph represented as an adjacency list.
  - **Process**:
    - Initialize an empty set `visited` to keep track of visited nodes.
    - Initialize an empty list `stack` to store the topological order of nodes.
    - Iterate over each node in the `adjacency_list`. If the node has not been visited, call `topological_sort_util` with the node and other required arguments.
    - After all nodes are processed, reverse the `stack` to obtain the correct topological order. This reversal is necessary because the dependencies need to be placed before the nodes that depend on them, and the stack was built bottom-up.
  - **Return**: The reversed `stack` list, which contains the nodes in their topological order.

This code is particularly useful for scheduling tasks, resolving dependencies, and other scenarios where a linear ordering of vertices in a directed graph is required, provided that the graph does not contain any cycles.



