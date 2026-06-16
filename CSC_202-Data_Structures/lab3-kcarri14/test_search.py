import unittest
import random
from lab3_p1 import linear_search, binary_search, compare_search, generate_random_lists

class TestSearchAlgorithms(unittest.TestCase):

    def setUp(self):
        self.num_lists = 10  # Smaller number for testing
        self.generated_lists = generate_random_lists(self.num_lists, 100, 1000, 1, 10000)

    def test_linear_search(self):
        for lst in self.generated_lists:
            target = lst[0]  # Choosing the first element as the target
            expected_comparisons = 1  # Should find it in the first comparison
            self.assertEqual(linear_search(lst, target), expected_comparisons)

    def test_binary_search(self):
        for lst in self.generated_lists:
            target = lst[0]  # Choosing the first element as the target
            comparisons = binary_search(lst, target)
            self.assertGreaterEqual(comparisons, 1)  # At least one comparison
            self.assertLessEqual(comparisons, len(lst))  # At most 'len(lst)' comparisons

    def test_comparison_difference(self):
        differences = []
        for lst in self.generated_lists:
            target = random.choice(lst)
            ls_comp, bs_comp, _ = compare_search(lst, target)
            differences.append(ls_comp - bs_comp)
        
        # Check if differences are calculated correctly
        for diff in differences:
            self.assertGreaterEqual(diff, 0)  # Linear search should always have more or equal comparisons

if __name__ == '__main__':
    unittest.main()
