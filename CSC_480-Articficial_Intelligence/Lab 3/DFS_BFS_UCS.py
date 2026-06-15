from collections import deque
import collections
from queue import PriorityQueue

def bfs(graph, start, goal):
    visited = set()
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)
    return False

# Example usage:
graph = {'A': {'B', 'C'}, 'B': {'A', 'D', 'E'}, 'C': {'A', 'F'}, 'D': {'B'}, 'E': {'B', 'F'}, 'F': {'C', 'E'}}
start_node = 'A'
goal_node = 'B'
print(bfs(graph, start_node, goal_node))

def dfs(graph, start, goal):
    visited = set()
    stack = collections.deque([start])

    while stack:
        node = stack.pop()
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node] - visited)
    return False  
      
(print(dfs (graph, start_node, goal_node)))

def ucs(graph, start, goal):
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, [start]))
    best_cost = {}


    while priority_queue:
        cost, node, path = priority_queue.get()
        if node == goal:
            return True, cost, path
        if node in best_cost and cost >= best_cost[node]:
            continue
        best_cost[node] = cost

        for nbr, w in graph.get(node, {}).items():
            priority_queue.put((cost + w, nbr, path + [nbr]))
    return False, 0, []
graph_w = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 5, 'D': 10},
    'C': {'A': 2, 'B': 5, 'D': 3},
    'D': {'B': 10, 'C': 3}
}
boolean, cost, path= ucs(graph_w, start_node, 'D')
print(boolean, cost, path)






