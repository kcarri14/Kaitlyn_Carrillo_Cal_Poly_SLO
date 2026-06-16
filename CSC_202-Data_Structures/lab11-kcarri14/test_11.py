import unittest
from lab11 import MinHeap

class TestMinHeap(unittest.TestCase):
    def setUp(self):
        self.min_heap = MinHeap()

    def test_enqueue_and_dequeue(self):
        # Test single enqueue and dequeue
        self.min_heap.enqueue((3, "Player A"))
        self.assertEqual(self.min_heap.dequeue(), (3, "Player A"))

    def test_multi_enqueue_and_dequeue(self):
        # Test multiple enqueues and dequeue order
        self.min_heap.enqueue((5, "Player B"))
        self.min_heap.enqueue((1, "Player C"))
        self.min_heap.enqueue((4, "Player D"))
        self.assertEqual(self.min_heap.dequeue(), (1, "Player C"))
        self.assertEqual(self.min_heap.dequeue(), (4, "Player D"))

    def test_multi_enqueue_and_dequeue_2(self):
        # Test the heap maintains min-heap property after multiple operations
        self.min_heap.enqueue((2, "Player E"))
        self.min_heap.enqueue((1, "Player F"))
        self.min_heap.enqueue((3, "Player G"))
        self.assertEqual(self.min_heap.dequeue(), (1, "Player F"))
        self.assertEqual(self.min_heap.dequeue(), (2, "Player E"))
        self.assertEqual(self.min_heap.dequeue(), (3, "Player G"))



if __name__ == '__main__':
    unittest.main()
