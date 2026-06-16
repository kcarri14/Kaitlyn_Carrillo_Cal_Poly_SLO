import unittest
from proj2 import bottomUpBFS, LinkedListQueue  # Ensure LinkedListQueue is accessible for the test

class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def queueToList(queue):
    """Convert a LinkedListQueue to a list."""
    result = []
    while not queue.isEmpty():
        result.append(queue.dequeue())
    return result


class TestBottomUpBFS(unittest.TestCase):
    def test_empty_tree(self):
        expected = LinkedListQueue()  # Expect an empty LinkedListQueue
        self.assertTrue(bottomUpBFS(None).isEmpty())

    def test_single_node(self):
        root = TreeNode(1)
        expected = [1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test_two_level_tree(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        expected = [2,3,1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test_three_level_tree(self):
        root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
        expected = [4,5,2,3,1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test_skewed_tree(self):
        # Creates a left-skewed tree
        root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4, TreeNode(5)))))
        expected = [5,4,3,2,1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)


    def test_right_skewed_tree(self):
        """Test a tree that extends to the right at every node"""
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3, None, TreeNode(4, None, TreeNode(5)))))
        expected = [5, 4, 3, 2, 1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test_single_child_each_level(self):
        """Test a tree where each node has a single child alternating between left and right"""
        root = TreeNode(1, TreeNode(2, None, TreeNode(3, TreeNode(4))), None)
        expected = [4, 3, 2, 1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test_complex_tree(self):
        """Test a more complex tree structure"""
        root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5, TreeNode(7))), TreeNode(3, None, TreeNode(6)))
        expected = [7, 4, 5, 6, 2, 3, 1]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)


if __name__ == "__main__":
    unittest.main()
