import unittest
from lab5 import ArrayStack
class TestArrayStack(unittest.TestCase):

    def setUp(self):
        # Common setup for each test case
        self.capacity = 5
        self.stack = ArrayStack(self.capacity)

    def test_push_and_pop(self):
        # Test pushing and then popping
        test_items = [1, 2, 3, 4, 5]
        for item in test_items:
            self.stack.push(item)

        for item in reversed(test_items):
            self.assertEqual(self.stack.pop(), item)

    def test_push_full_stack(self):
        # Test pushing into a full stack
        for i in range(self.capacity):
            self.stack.push(i)

        with self.assertRaises(Exception) as context:
            self.stack.push(6)
        self.assertTrue('Stack is full' in str(context.exception))

    def test_pop_empty_stack(self):
        # Test popping from an empty stack
        with self.assertRaises(Exception) as context:
            self.stack.pop()
        self.assertTrue('Stack is empty' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
