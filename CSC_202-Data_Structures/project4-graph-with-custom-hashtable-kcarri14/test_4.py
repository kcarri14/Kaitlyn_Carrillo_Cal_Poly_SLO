import unittest
from p4 import Hashtable, Graph

class TestHashtable(unittest.TestCase):
    def test_insert_and_get(self):
        """Test that inserting and then getting the value works correctly."""
        ht = Hashtable(capacity=5)
        ht.insert('A', 'Alpha')
        self.assertEqual(ht.get('A'), 'Alpha')

    def test_delete(self):
        """Test that deleting an item works correctly."""
        ht = Hashtable(capacity=5)
        ht.insert('A', 'Alpha')
        ht.delete('A')
        self.assertIsNone(ht.get('A'))

    def test_collision_and_probing(self):
        """Test that linear probing resolves collisions correctly."""
        ht = Hashtable(capacity=5)
        # These keys should result in a collision based on the hash function
        ht.insert('A', 'Alpha')
        ht.insert('F', 'Foxtrot')  # 'F' and 'A' have the same hash in a small table
        self.assertEqual(ht.get('F'), 'Foxtrot')
        self.assertNotEqual(ht.get('A'), 'Foxtrot')

class TestGraph(unittest.TestCase):
    def setUp(self):
        """Set up a graph for testing."""
        self.graph = Graph(vertices=5)
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('A', 'C')
        self.graph.add_edge('B', 'D')
        self.graph.add_edge('C', 'E')

    def test_add_edge(self):
        """Test that edges are added correctly."""
        self.assertIn('B', self.graph.graph.get('A'))
        self.assertIn('A', self.graph.graph.get('B'))

    def test_dfs_traversal(self):
        """Test that DFS traversal visits all vertices."""
        visited = set()
        # Starting from 'A', we should visit all vertices.
        expected = {'A', 'B', 'C', 'D', 'E'}
        self.graph.dfs_traversal('A', visited)
        self.assertEqual(visited, expected)

if __name__ == '__main__':
    unittest.main()
