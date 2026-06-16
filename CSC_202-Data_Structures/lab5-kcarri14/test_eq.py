import unittest
from lab5 import DoublyLinkedList

class TestEq(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(3):
            self.dll.append(i)

    def test_eq_true(self):
        other_dll = DoublyLinkedList()
        for i in range(3):
            other_dll.append(i)
        self.assertTrue(self.dll == other_dll)

    def test_eq_false_different_lengths(self):
        other_dll = DoublyLinkedList()
        for i in range(2):
            other_dll.append(i)
        self.assertFalse(self.dll == other_dll)

    def test_eq_false_different_data(self):
        other_dll = DoublyLinkedList()
        for i in range(3):
            other_dll.append(i + 1)  # Different data
        self.assertFalse(self.dll == other_dll)

    def test_eq_with_non_list_object(self):
        self.assertFalse(self.dll == [0, 1, 2])  # Comparing with a regular list

    def test_eq_empty_lists(self):
        empty_dll1 = DoublyLinkedList()
        empty_dll2 = DoublyLinkedList()
        self.assertTrue(empty_dll1 == empty_dll2)

    def test_eq_empty_and_non_empty_list(self):
        empty_dll = DoublyLinkedList()
        self.assertFalse(self.dll == empty_dll)

if __name__ == '__main__':
    unittest.main()
