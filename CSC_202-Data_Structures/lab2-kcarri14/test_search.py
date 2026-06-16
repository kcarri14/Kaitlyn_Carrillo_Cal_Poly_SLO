import unittest
from lab2 import bin_search

class TestBinSearch(unittest.TestCase):

    def test_search_found(self):
        self.assertEqual(bin_search(4, 0, 4, [1, 2, 3, 4, 5]), 3)

    def test_search_not_found(self):
        self.assertIsNone(bin_search(6, 0, 4, [1, 2, 3, 4, 5]))

    def test_search_empty(self):
        self.assertIsNone(bin_search(1, 0, 0, []))

    def test_search_single_element(self):
        self.assertEqual(bin_search(1, 0, 0, [1]), 0)

    def test_search_raises_value_error(self):
        with self.assertRaises(ValueError):
            bin_search(1, 0, 1, None)

if __name__ == '__main__':
    unittest.main()
