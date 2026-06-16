import unittest
import random
from lab7 import LinkedListQueue, sort_linked_list_queue_correctly

class TestLinkedListQueue(unittest.TestCase):

    def setUp(self):
        self.queue = LinkedListQueue()
    
    def test_enqueue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.assertEqual(self.queue.to_list(), [3, 2, 1], "Enqueue method should add items to the rear.")

    def test_dequeue(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.dequeue()
        self.assertEqual(self.queue.to_list(), [2], "Dequeue method should remove the front item.")

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty(), "Queue should be empty initially.")
        self.queue.enqueue(1)
        self.assertFalse(self.queue.is_empty(), "Queue should not be empty after enqueue.")

    def test_peek_front(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.peek_front(), 1, "Peek front should return the front item without removing it.")

    def test_sort_linked_list_queue_correctly(self):
        for card in [1,2,3,4,5,6,7,8,9,10,11,12,13]:
            self.queue.enqueue(card)
        sorted_queue = sort_linked_list_queue_correctly(self.queue)
        self.assertEqual(sorted_queue.to_list(), [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 
                         "Sort function should sort queue from high to low.")

    def test_enqueue_dequeue_sequence(self):
        for i in range(5):
            self.queue.enqueue(i)
        for i in range(5):
            self.assertEqual(self.queue.dequeue(), i, f"Dequeue should return {i} in sequence.")

    def test_dequeue_empty_queue(self):
        self.assertIsNone(self.queue.dequeue(), "Dequeue on an empty queue should return None.")

    def test_to_list_empty_queue(self):
        self.assertEqual(self.queue.to_list(), [], "to_list on an empty queue should return an empty list.")

    def test_sort_with_random_order(self):
        cards = [i for i in range(1, 14)]
        random.shuffle(cards)
        for card in cards:
            self.queue.enqueue(card)
        sorted_queue = sort_linked_list_queue_correctly(self.queue)
        self.assertEqual(sorted_queue.to_list(), list(range(1,14))[::-1], 
                         "Sort function should correctly sort a randomly ordered queue.")






if __name__ == '__main__':
    unittest.main()
