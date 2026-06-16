import unittest
from lab5 import DoublyLinkedList

class TestSetItem(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(1, 5):  # List will be 1, 2, 3, 4
            self.dll.append(i)

    def test_set_first_item(self):
        self.dll[0] = 10
        self.assertEqual(self.dll[0], 10)

    def test_set_middle_item(self):
        self.dll[2] = 30
        self.assertEqual(self.dll[2], 30)

    def test_set_last_item(self):
        self.dll[3] = 40
        self.assertEqual(self.dll[3], 40)

    def test_set_invalid_positive_index(self):
        with self.assertRaises(IndexError):
            self.dll[10] = 100

    def test_set_invalid_negative_index(self):
        with self.assertRaises(IndexError):
            self.dll[-1] = 100

    def test_set_item_in_empty_list(self):
        empty_dll = DoublyLinkedList()
        with self.assertRaises(IndexError):
            empty_dll[0] = 100

if __name__ == '__main__':
    unittest.main()
