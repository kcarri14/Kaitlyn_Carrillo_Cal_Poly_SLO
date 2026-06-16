import unittest
from lab14 import find_adj_matrix1, find_adj_matrix2, find_adj_list1, find_adj_list2, bfs, topological_sort

class TestGraphFunctions(unittest.TestCase):
    def test_find_adj_matrix1(self):
        expected = [
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1],
            [0, 1, 1, 0, 1, 0]
        ]
        self.assertEqual(find_adj_matrix1(), expected)

    def test_find_adj_matrix2(self):
        expected = [
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0]
        ]
        self.assertEqual(find_adj_matrix2(), expected)

    def test_find_adj_list1(self):
        expected = {
            'A': {'C'},
            'C': {'A', 'D', 'F'},
            'D': {'C', 'B'},
            'F': {'C', 'B', 'E'},
            'B': {'D', 'F', 'E'},
            'E': {'B', 'F', 'E'}
        }
        self.assertEqual(find_adj_list1(), expected)

    def test_adjacency_list2(self):
        expected = {
            '1': {'2', '3'},
            '2': {'4'},
            '3': {'4'},
            '4': {'5'},
            '5': {}
        }
        self.assertEqual(find_adj_list2(), expected)
    
    def test_bfs_order(self):
        adjacency_list = {
            'A': {'C'},
            'C': {'A', 'D', 'F'},
            'D': {'C', 'B'},
            'F': {'C', 'B', 'E'},
            'B': {'D', 'F', 'E'},
            'E': {'B', 'F', 'E'}
        }
        expected_order = ['A', 'C', 'D', 'F', 'B', 'E']
        result = bfs(adjacency_list, 'A')
        self.assertEqual(result, expected_order)



    def test_topological_sort(self):
        adjacency_list = {
            '1': {'2', '3'},
            '2': {'4'},
            '3': {'4'},
            '4': {'5'}
        }
        # A possible valid topological order for the given graph
        expected_order = ['1', '3', '2', '4', '5']
        result = topological_sort(adjacency_list)
        self.assertEqual(result, expected_order)



if __name__ == '__main__':
    unittest.main()
