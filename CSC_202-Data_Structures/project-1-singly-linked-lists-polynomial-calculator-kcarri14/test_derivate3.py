import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialDifferentiationEdgeCases(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def create_linked_list(self, coefficients):
        ll = LinkedList()
        for coeff in coefficients:
            ll.append(coeff)
        return ll

    def test_differentiate_non_linked_list(self):
        poly = [1, 2, 3]  # Not a linked list
        with self.assertRaises(TypeError):
            self.calc.differentiate_polynomial(poly)

    def test_differentiate_with_none_head(self):
        poly = None  # None head
        with self.assertRaises(TypeError):
            self.calc.differentiate_polynomial(poly)

    def test_differentiate_with_none_val(self):
        poly = self.create_linked_list([None, 2, 3])  # None value in node
        with self.assertRaises(TypeError):
            self.calc.differentiate_polynomial(poly.head)

    def test_differentiate_with_non_numeric_val(self):
        poly = self.create_linked_list(["a", 2, 3])  # Non-numeric value
        with self.assertRaises(TypeError):
            self.calc.differentiate_polynomial(poly.head)

    def test_differentiate_with_single_term(self):
        poly = self.create_linked_list([5])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_with_single_zero_term(self):
        poly = self.create_linked_list([0])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_with_all_zero_terms(self):
        poly = self.create_linked_list([0, 0, 0])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_with_alternating_signs(self):
        poly = self.create_linked_list([1, -2, 3, -4])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.create_linked_list([3, -4, 3]).head.val, result.val)

    def test_differentiate_with_constant_term_only(self):
        poly = self.create_linked_list([3])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
