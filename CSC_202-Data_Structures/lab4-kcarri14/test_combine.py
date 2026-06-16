import unittest
from lab4 import LinkedList, combine_linked_lists

class TestCombineLinkedLists(unittest.TestCase):
    def setUp(self):
        self.list1 = LinkedList()
        self.list2 = LinkedList()

        for i in range(1, 4):  # List 1: 1 -> 2 -> 3
            self.list1.append(i)
        for i in range(4, 7):  # List 2: 4 -> 5 -> 6
            self.list2.append(i)

    def test_combine_non_empty_lists(self):
        combined = combine_linked_lists(self.list1, self.list2)
        self.assertEqual(str(combined), '1 -> 2 -> 3 -> 4 -> 5 -> 6')

    def test_combine_empty_and_non_empty_list(self):
        empty_list = LinkedList()
        combined = combine_linked_lists(empty_list, self.list2)
        self.assertEqual(str(combined), '4 -> 5 -> 6')

    def test_combine_non_empty_and_empty_list(self):
        empty_list = LinkedList()
        combined = combine_linked_lists(self.list1, empty_list)
        self.assertEqual(str(combined), '1 -> 2 -> 3')

    def test_combine_with_non_linked_list_objects(self):
        with self.assertRaises(TypeError):
            combine_linked_lists(self.list1, "not a linked list")

    def test_combine_with_none_argument(self):
        with self.assertRaises(TypeError):
            combine_linked_lists(self.list1, None)

if __name__ == '__main__':
    unittest.main()
