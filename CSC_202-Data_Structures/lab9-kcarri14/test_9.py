import unittest
from lab9 import sortedListToBST, isValidBST, areSameTree, TreeNode 
from collections import deque

def createBinaryTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

class TestSortedArrayToBST(unittest.TestCase):
    def test_sorted_list_to_bst(self):
        # Assuming a function 'sortedListToBST' exists
        result = sortedListToBST([-10, -3, 0, 5, 9])
        # Verify the structure and values of the BST
        # This will be specific to your implementation
        self.assertEqual(result.value, 0)  # Example check
        # Add more checks to verify the BST structure and values
        # This can include checking the height, left/right values, etc.

class TestIsValidBST(unittest.TestCase):
    def test_is_valid_bst(self):
        # Assuming a function 'isValidBST' exists
        # Assuming a helper method 'createBST' to create a BST from values
        bst = createBinaryTree([2, 1, 3])  # Create a valid BST for testing
        self.assertTrue(isValidBST(bst))
        
        bst = createBinaryTree([5, 1, 4, None, None, 3, 6])  # Create an invalid BST
        self.assertFalse(isValidBST(bst))

# Add additional test methods to cover edge cases, like an empty tree or a tree with one node


class TestAreSameTree(unittest.TestCase):
    def test_are_same_tree(self):
        # Assuming a function 'areSameTree' exists
        # Assuming a helper method 'createBinaryTree' to create a binary tree from values
        tree1 = createBinaryTree([1, 2, 3])  # Create tree 1
        tree2 = createBinaryTree([1, 2, 3])  # Create an identical tree 2
        self.assertTrue(areSameTree(tree1, tree2))
        
        tree3 = createBinaryTree([1, 2])  # Create a different tree 3
        self.assertFalse(areSameTree(tree1, tree3))



if __name__ == '__main__':
    unittest.main()