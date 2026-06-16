import unittest
from lab4 import LinkedList, is_palindrome

class TestIsPalindrome(unittest.TestCase):
    def create_list(self, elements):
        llist = LinkedList()
        for element in elements:
            llist.append(element)
        return llist

    def test_palindrome_odd(self):
        llist = self.create_list(['a', 'b', 'a'])
        self.assertTrue(is_palindrome(llist))

    def test_palindrome_even(self):
        llist = self.create_list(['n', 'o', 'o', 'n'])
        self.assertTrue(is_palindrome(llist))

    def test_not_palindrome(self):
        llist = self.create_list(['h', 'e', 'l', 'l', 'o'])
        self.assertFalse(is_palindrome(llist))

    def test_empty_list(self):
        llist = LinkedList()
        self.assertFalse(is_palindrome(llist))

    def test_none_input(self):
        self.assertFalse(is_palindrome(None))

if __name__ == '__main__':
    unittest.main()
