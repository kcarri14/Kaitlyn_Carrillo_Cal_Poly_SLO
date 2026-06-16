import unittest
from lab2 import reverse_rec

class TestReverseRec(unittest.TestCase):

    def test_reverse_normal(self):
        self.assertEqual(reverse_rec([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])

    def test_reverse_empty(self):
        self.assertEqual(reverse_rec([]), [])

    def test_reverse_single_element(self):
        self.assertEqual(reverse_rec([1]), [1])

    def test_reverse_negative(self):
        self.assertEqual(reverse_rec([-5, -4, -3]), [-3, -4, -5])

    def test_reverse_raises_value_error(self):
        with self.assertRaises(ValueError):
            reverse_rec(None)

if __name__ == '__main__':
    unittest.main()
