import unittest
from lab5 import reverse_stack, ArrayStack

class TestReverseStack(unittest.TestCase):

    def test_reverse_stack_non_empty(self):
        # Test with a non-empty stack
        stack = ArrayStack(5)
        for item in [1, 2, 3, 4, 5]:
            stack.push(item)

        reversed_stack = reverse_stack(stack)
        reversed_items = [reversed_stack.pop() for _ in range(reversed_stack.size())]
        self.assertEqual(reversed_items, [1,2,3,4,5])

    def test_reverse_stack_empty(self):
        # Test with an empty stack
        empty_stack = ArrayStack(5)
        reversed_empty_stack = reverse_stack(empty_stack)
        self.assertTrue(reversed_empty_stack.is_empty())

    def test_reverse_stack_single_element(self):
        # Test with a stack having a single element
        stack = ArrayStack(5)
        stack.push(1)

        reversed_stack = reverse_stack(stack)
        self.assertEqual(reversed_stack.pop(), 1)
        self.assertTrue(reversed_stack.is_empty())

    def test_reverse_stack_repeating_elements(self):
        # Test with a stack having repeating elements
        stack = ArrayStack(5)
        for item in [2, 2, 2, 2, 2]:
            stack.push(item)

        reversed_stack = reverse_stack(stack)
        reversed_items = [reversed_stack.pop() for _ in range(reversed_stack.size())]
        self.assertEqual(reversed_items, [2, 2, 2, 2, 2])

    def test_reverse_stack_full_capacity(self):
        # Test with a stack at full capacity
        stack = ArrayStack(3)
        for item in [1, 2, 3]:
            stack.push(item)

        reversed_stack = reverse_stack(stack)
        reversed_items = [reversed_stack.pop() for _ in range(reversed_stack.size())]
        self.assertEqual(reversed_items, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()
