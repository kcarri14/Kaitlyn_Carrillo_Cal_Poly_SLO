import unittest
from lab5 import reverse_stack, process_card_stack, ArrayStack
import random
class TestArrayStack(unittest.TestCase):

    def setUp(self):
        # Common setup for each test case
        self.capacity = 7
        self.solution_capacity = 13
        self.stack = ArrayStack(self.capacity)

    def test_push_and_pop(self):
        # Test pushing and then popping
        test_items = [10, 20, 35, 44, 53, 67, 34]
        for item in test_items:
            self.stack.push(item)

    def test_pop(self):
        #second test pushing then popping
        test_items = [1, 20, 35, 4, 53, 67, 4]
        for item in test_items:
            self.stack.push(item)
        for item in reversed(test_items):
            self.assertEqual(self.stack.pop(), item)

    def test_push(self):
        #test the pushing function
        test_items = [1,2,3,4,5,6,7]
        for item in test_items:
            self.stack.push(item)  

    def test_push2(self):
        #test the pushing function again
        test_items = [46,50,64,72,84,96,1023]
        for item in test_items:
            self.stack.push(item)  

    def test_reverse_stack_repeating_elements(self):
        # Test with a stack having repeating elements
        stack = ArrayStack(7)
        for item in [2, 3, 4, 4, 3, 2]:
            stack.push(item)

        reversed_stack = reverse_stack(stack)
        reversed_items = [reversed_stack.pop() for _ in range(reversed_stack.size())]
        self.assertEqual(reversed_items, [2, 3, 4, 4, 3,2])

    def test_reverse_stack_empty(self):
        # Test with an empty stack
        empty_stack = ArrayStack(5)
        reversed_empty_stack = reverse_stack(empty_stack)
        self.assertTrue(reversed_empty_stack.is_empty())    
                    

    def test_push_full_stack(self):
        # Test pushing into a full stack
        for i in range(self.capacity):
            self.stack.push(i)

        with self.assertRaises(Exception) as context:
            self.stack.push(8)
        self.assertTrue('Stack is full' in str(context.exception))

    def test_pop_empty_stack(self):
        # Test popping from an empty stack
        with self.assertRaises(Exception) as context:
            self.stack.pop()
        self.assertTrue('Stack is empty' in str(context.exception))

    def test_process_sort(self):
        cardStack = ArrayStack(self.solution_capacity)
        cards = [i for i in range(1, 14)]
        random.shuffle(cards)
        for card in cards:
            cardStack.push(card)
        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1,14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])

    def test_process_sort_2(self):
        cardStack = ArrayStack(self.solution_capacity)
        cards = [i for i in range(1, 14)]
        random.shuffle(cards)
        for card in cards:
            cardStack.push(card)
        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1,14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])    

if __name__ == '__main__':
    unittest.main()
