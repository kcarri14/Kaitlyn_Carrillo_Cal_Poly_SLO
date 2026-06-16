import unittest
from lab5 import process_card_stack, ArrayStack
import random

class TestProcessCardStack(unittest.TestCase):

    def setUp(self):
        # Common setup for each test case
        self.solution_capacity = 13

    def test_correct_order(self):
        # Test with cards in random order
        cardStack = ArrayStack(self.solution_capacity)
        for card in [3, 6, 4, 1, 2, 5, 9, 8, 7, 10, 13, 12, 11]:
            cardStack.push(card)

        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1,14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])

    def test_already_sorted(self):
        # Test with cards already in correct order
        cardStack = ArrayStack(self.solution_capacity)
        for card in range(1, 14):
            cardStack.push(card)

        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1, 14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])

    
    def test_3(self):
        cardStack = ArrayStack(self.solution_capacity)
        cards = [i for i in range(1, 14)]
        random.shuffle(cards)
        for card in cards:
            cardStack.push(card)
        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1,14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])

    def test_4(self):
        cardStack = ArrayStack(self.solution_capacity)
        cards = [i for i in range(1, 14)]
        random.shuffle(cards)
        for card in cards:
            cardStack.push(card)
        result = process_card_stack(cardStack)
        expected_solution = [i for i in range(1,14)]
        actual_solution = [result.pop() for _ in range(result.size())]
        self.assertEqual(actual_solution, expected_solution[::-1])


    def test_none_input(self):
        # Test with None input
        with self.assertRaises(TypeError):
            process_card_stack(None)

    def test_non_stack_input(self):
        # Test with input that is not a stack
        non_stack_input = [1, 2, 3, 4, 5]
        with self.assertRaises(TypeError):
            process_card_stack(non_stack_input)

    def test_incorrect_size(self):
        # Test with stack size not equal to 13
        incorrect_size_stack = ArrayStack(10)
        for card in range(1, 11):
            incorrect_size_stack.push(card)
        with self.assertRaises(ValueError):
            process_card_stack(incorrect_size_stack)


if __name__ == '__main__':
    unittest.main()
