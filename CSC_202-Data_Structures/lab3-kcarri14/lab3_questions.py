#Answer these Questions
def best_case_ls():
    #what is the best case for linear search?
    a = "when target is at the beginning"
    b = "when target is at the end"
    return a

def worst_case_ls():
    #what is the worst case for linear search?
    a = "when target is at the beginning"
    b = "when target is at the end"
    return b
  

def best_case_bs():
    #what is the best case for binary search?
    a = "when target is at the midpoint"
    b = "when target is at the limits"
    return a

def worst_case_bs():
    #what is the best case for binary search?
    a = "when target is at the midpoint"
    b = "when target is at the limits"
    return b

def selection_vs_insertion():
    #why might insertion sort perform faster than selection sort?
    a = "insertion sort might perform fewer swaps than selection"
    b = "insertion sort has a better time complexity"
    return a


import unittest
from lab3_questions import best_case_ls, best_case_bs, worst_case_bs, worst_case_ls, selection_vs_insertion

class TestSearchSortAlgorithms(unittest.TestCase):

    def test_best_case_ls(self):
        self.assertEqual(best_case_ls(), "when target is at the beginning")

    def test_worst_case_ls(self):
        self.assertEqual(worst_case_ls(), "when target is at the end")

    def test_best_case_bs(self):
        self.assertEqual(best_case_bs(), "when target is at the midpoint")

    def test_worst_case_bs(self):
        self.assertEqual(worst_case_bs(), "when target is at the limits")

    def test_selection_vs_insertion(self):
        self.assertEqual(selection_vs_insertion(), "insertion sort might perform fewer swaps than selection")

if __name__ == '__main__':
    unittest.main()