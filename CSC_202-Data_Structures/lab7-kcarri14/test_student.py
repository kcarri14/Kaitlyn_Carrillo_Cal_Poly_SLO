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
        for card in [3,4,6,1,2,6,11,8,13,9,10,5,12,7]:
            self.queue.enqueue(card)
        sorted_queue = sort_linked_list_queue_correctly(self.queue)
        self.assertEqual(sorted_queue.to_list(), [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 
                         "Sort function should sort queue from high to low.")