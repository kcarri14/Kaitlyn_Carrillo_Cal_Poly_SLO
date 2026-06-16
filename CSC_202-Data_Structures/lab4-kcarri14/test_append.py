

import unittest
from lab4 import LinkedList

class TestLinkedList(unittest.TestCase):
    def test_append_to_empty_list(self):
        llist = LinkedList()
        llist.append(1)
        self.assertEqual(str(llist), '1')

    def test_append_multiple_elements(self):
        llist = LinkedList()
        llist.append(1)
        llist.append(2)
        llist.append(3)
        self.assertEqual(str(llist), '1 -> 2 -> 3')

    def test_append_string(self):
        llist = LinkedList()
        llist.append("Hello")
        self.assertEqual(str(llist), 'Hello')

    def test_append_none(self):
        llist = LinkedList()
        llist.append(None)
        self.assertEqual(str(llist), 'None')

if __name__ == '__main__':
    unittest.main()
