import random
import time
from collections import deque
import collections
from queue import PriorityQueue

def generate_random_grid(size, prob):
    grid = []
    for i in range(size):
        row = [0 if random.random() > prob else 1 for _ in range(size)]
        grid.append(row)
    grid[0][0] = 0  
    grid[size - 1][size - 1] = 0 
    return grid

def print_grid(grid, path):
    size = len(grid)
    for i in range(size):
        row = ""
        for j in range(size):
            if path and (i, j) in path:
                row += "y"
            elif grid[i][j] == 1:
                row += "X"
            else:
                row += "x"
        print(row)
    print()

def get_neighbors(pos, grid):
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(came, goal):
    path = [goal]
    while goal in came:
        goal = came[goal]
        path.append(goal)
    path.reverse()
    return path    

def bfs(grid, start, goal):
    start_time = time.time()
    came_from = {}
    nodes_explored = 0
    visited = {start} 
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        nodes_explored +=1

        if node == goal:
            elapsed = time.time() - start_time
            return reconstruct_path(came_from, goal), nodes_explored, elapsed
        
        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = node
                queue.append(neighbor)

    return None, nodes_explored, time.time() - start_time

def dfs(grid, start, goal):
    start_time = time.time()
    came_from = {}
    nodes_explored = 0
    visited = {start} 
    stack = collections.deque([start])

    while stack:
        node = stack.pop()
        nodes_explored += 1
        if node == goal:
            elapsed = time.time() - start_time
            return reconstruct_path(came_from, goal), nodes_explored, elapsed
        for neighbor in get_neighbors(node, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = node
                stack.append(neighbor)

    return None, nodes_explored, time.time() - start_time  
      

def ucs(grid, start, goal):
    start_time = time.time()
    came_from = {}
    nodes_explored = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, start))
    best_cost = {start: 0}


    while not priority_queue.empty():
        cost, node = priority_queue.get()
        nodes_explored +=1
        if node == goal:
            elapsed = time.time() - start_time
            return reconstruct_path(came_from, goal), nodes_explored, elapsed

        for neighbor in get_neighbors(node, grid):
            new_cost = best_cost[node] + 1  
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                came_from[neighbor] = node
                priority_queue.put((new_cost, neighbor))

    return None, nodes_explored, time.time() - start_time

def compare_algorithms(size, prob):
    #print("we here")
    grid = generate_random_grid(size, prob)
    start = (0, 0)
    free_cells = [(i, j) for i in range(size) for j in range(size) if grid[i][j] == 0 and (i, j) != start]

    if free_cells:
        goal = random.choice(free_cells)
    

    print(f"Goal: {goal}")
    print_grid(grid, None)

    algorithms = [("BFS", bfs), ("DFS", dfs), ("UCS", ucs)]

    for name, func in algorithms:
        #print("here")
        path, nodes, elapsed = func(grid, start, goal)

        if path:
            print(f"{name}")
            print(f"Path found: {len(path)} steps")
            print(f"Time it took: {elapsed:.5f}")
            print(f"Nodes explored: {nodes}")
            print_grid(grid, path)
        else:
            print("No path")

if __name__ == "__main__":
    compare_algorithms(10, 0.25)            
