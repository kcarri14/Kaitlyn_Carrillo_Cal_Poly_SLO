def find_adj_matrix1():
    matrix1 = [[0, 0, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1],
               [1, 0, 0, 1, 0, 1],
               [0, 1, 1, 0, 0, 0],
               [0, 1, 0, 0, 1, 1],
               [0, 1, 1, 0, 1, 0]
               ]
    return matrix1
def find_adj_matrix2():  
    matrix2 = [[0, 1, 1, 0, 0],
               [0, 0, 0, 1, 0],
               [0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0]]
    return matrix2
def find_adj_list1():
    list1 = {
        'A': {'C'},
        'B': {'D','E','F'},
        'C': {'A','D','F'},
        'D': {'B','C'},
        'E': {'B','F','E'},
        'F': {'B','C','E'}
    }
    return list1
def find_adj_list2():
    list2 = {
        '1': {'2','3'},
        '2': {'4'},
        '3': {'4'},
        '4': {'5'},
        '5': {}
    }
    return list2
def bfs(adjacency_list, start_vertex):
   visited = list()
   queue = [start_vertex]
   bfs_order = []

   while queue:
    current = queue.pop(0)
    if current  not in visited:
        bfs_order.append(current)
        visited.append(current)
        for neighbor in adjacency_list[current]:
            if neighbor not in visited:
                queue.append(neighbor)

   return bfs_order

def topological_sort_util(node, visited, stack, adjacency_list):
    visited.append(node)
    if node in adjacency_list:
        for neighbor in adjacency_list[node]:
            if neighbor not in visited:
                topological_sort_util(neighbor, visited, stack, adjacency_list)
                stack.append(node)
   

def topological_sort(adjacency_list):
    visited = list()
    stack = []

    for neighbor in adjacency_list:
            if neighbor not in visited:
                topological_sort_util(neighbor, visited, stack, adjacency_list)
    stack.reverse()
    return stack



