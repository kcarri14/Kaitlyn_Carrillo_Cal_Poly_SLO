import unittest
from lab5 import DoublyLinkedList

class TestGetItem(unittest.TestCase):
    

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(2, 6):  # List will be 1, 2, 3, 4
            self.dll.append(i)

    def test_get_first_item(self):
        self.assertEqual(self.dll[0], 2)

    def test_get_middle_item(self):
        self.assertEqual(self.dll[2], 4)

    def test_get_last_item(self):
        self.assertEqual(self.dll[3], 5)

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

class TestEq(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(5):
            self.dll.append(i)

    def test_eq_true(self):
        other_dll = DoublyLinkedList()
        for i in range(5):
            other_dll.append(i)
        self.assertTrue(self.dll == other_dll)

    def test_eq_false_different_lengths(self):
        other_dll = DoublyLinkedList()
        for i in range(4):
            other_dll.append(i)
        self.assertFalse(self.dll == other_dll)

    def test_eq_false_different_data(self):
        other_dll = DoublyLinkedList()
        for i in range(5):
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

class TestSetItem(unittest.TestCase):

    def setUp(self):
        self.dll = DoublyLinkedList()
        for i in range(5, 10):  # List will be 1, 2, 3, 4
            self.dll.append(i)

    def test_set_first_item(self):
        self.dll[0] = 50
        self.assertEqual(self.dll[0], 50)

    def test_set_middle_item(self):
        self.dll[2] = 70
        self.assertEqual(self.dll[2], 70)

    def test_set_last_item(self):
        self.dll[3] = 90
        self.assertEqual(self.dll[3], 90)

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