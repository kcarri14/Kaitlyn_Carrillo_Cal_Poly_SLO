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
    def test1(self):
        root = TreeNode(4, TreeNode(5), TreeNode(6))
        expected = [5,6,4]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test2(self):
        root = TreeNode(2, TreeNode(3, TreeNode(5), TreeNode(6)), TreeNode(4))
        expected = [5,6,3,4,2]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)

    def test3(self):
        root = TreeNode(2, TreeNode(3, TreeNode(4, TreeNode(5, TreeNode(6)))))
        expected = [6,5,4,3,2]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)
    def test4(self):
        root = TreeNode(3, TreeNode(4, TreeNode(6), TreeNode(7, TreeNode(9))), TreeNode(5, None, TreeNode(8)))
        expected = [9, 6, 7, 8, 4, 5, 3]
        self.assertEqual(queueToList(bottomUpBFS(root)), expected)    

if __name__ == "__main__":
    unittest.main()