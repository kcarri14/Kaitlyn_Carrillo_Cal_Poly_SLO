import unittest
from lab3_p2 import insertion_sort, selection_sort  

class TestSortingAlgorithms(unittest.TestCase):

    def test_insertion_sort_random(self):
        lst = [5, 3, 8, 6, 7]
        self.assertEqual(insertion_sort(lst), sorted(lst))

    def test_insertion_sort_sorted(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(insertion_sort(lst), sorted(lst))

    def test_insertion_sort_reverse(self):
        lst = [5, 4, 3, 2, 1]
        self.assertEqual(insertion_sort(lst), sorted(lst))

    def test_insertion_sort_empty(self):
        lst = []
        self.assertEqual(insertion_sort(lst), sorted(lst))

    def test_insertion_sort_identical(self):
        lst = [1, 1, 1, 1]
        self.assertEqual(insertion_sort(lst), sorted(lst))

    def test_selection_sort_random(self):
        lst = [5, 3, 8, 6, 7]
        self.assertEqual(selection_sort(lst), sorted(lst))

    def test_selection_sort_sorted(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(selection_sort(lst), sorted(lst))

    def test_selection_sort_reverse(self):
        lst = [5, 4, 3, 2, 1]
        self.assertEqual(selection_sort(lst), sorted(lst))

    def test_selection_sort_empty(self):
        lst = []
        self.assertEqual(selection_sort(lst), sorted(lst))

    def test_selection_sort_identical(self):
        lst = [1, 1, 1, 1]
        self.assertEqual(selection_sort(lst), sorted(lst))

if __name__ == '__main__':
    unittest.main()
