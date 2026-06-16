import unittest
from lab2 import max_list_iter, reverse_rec, bin_search

class TestLab2(unittest.TestCase):

    # Tests for max_list_iter
    def test_max_list_iter_custom1(self):
        self.assertEqual(max_list_iter([2,5,76,8,45,9,98]), 98)

    def test_max_list_iter_custom2(self):
        self.assertEqual(max_list_iter([2,-3,4,-15,34,86,-100]), 86)  

    # Tests for reverse_rec
    def test_reverse_rec_custom1(self):
        self.assertEqual(reverse_rec([1, 2]), [2, 1])

    def test_reverse_rec_custom2(self):
        self.assertEqual(reverse_rec([-1, 2, 4, -5, 6, 7, 12]), [12,7,6,-5,4,2,-1])

        pass

    # Tests for bin_search
    def test_bin_search_custom1(self):
        self.assertEqual(bin_search(7, 0, 6, [1, 20, 3, -4, 5,7,98]), 5)
        pass

    def test_bin_search_custom2(self):
        self.assertEqual(bin_search(20, 0, 1, [1, 20]), 1)
        pass

if __name__ == '__main__':
    unittest.main()
