import unittest
from lab2 import max_list_iter

class TestMaxListIter(unittest.TestCase):

    def test_max_normal(self):
        self.assertEqual(max_list_iter([1, 2, 3, 4, 5]), 5)

    def test_max_empty(self):
        self.assertIsNone(max_list_iter([]))

    def test_max_single_element(self):
        self.assertEqual(max_list_iter([4]), 4)

    def test_max_negative(self):
        self.assertEqual(max_list_iter([-3, -1, -2]), -1)

    def test_max_raises_value_error(self):
        with self.assertRaises(ValueError):
            max_list_iter(None)

if __name__ == '__main__':
    unittest.main()
