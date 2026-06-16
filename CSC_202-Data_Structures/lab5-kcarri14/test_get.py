import unittest
from lab5 import DoublyLinkedList

class TestGetItem(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(1, 5):  # List will be 1, 2, 3, 4
            self.dll.append(i)

    def test_get_first_item(self):
        self.assertEqual(self.dll[0], 1)

    def test_get_middle_item(self):
        self.assertEqual(self.dll[2], 3)

    def test_get_last_item(self):
        self.assertEqual(self.dll[3], 4)

    def test_get_invalid_positive_index(self):
        with self.assertRaises(IndexError):
            _ = self.dll[10]

    def test_get_invalid_negative_index(self):
        with self.assertRaises(IndexError):
            _ = self.dll[-1]

    def test_get_item_from_empty_list(self):
        empty_dll = DoublyLinkedList()
        with self.assertRaises(IndexError):
            _ = empty_dll[0]

if __name__ == '__main__':
    unittest.main()
