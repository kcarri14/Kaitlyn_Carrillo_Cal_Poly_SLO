import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialAntiDerivativeEdgeCases(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def create_linked_list(self, coefficients):
        ll = LinkedList()
        for coeff in coefficients:
            ll.append(coeff)
        return ll

    def test_anti_derivative_non_linked_list(self):
        poly = [1, 2, 3]  # Not a linked list
        with self.assertRaises(TypeError):
            self.calc.anti_derivative_polynomial(poly)

    def test_anti_derivative_with_none_head(self):
        poly = None  # None head
        with self.assertRaises(TypeError):
            self.calc.anti_derivative_polynomial(poly)

    def test_anti_derivative_with_none_val(self):
        poly = self.create_linked_list([None, 2, 3])  # None value in node
        with self.assertRaises(TypeError):
            self.calc.anti_derivative_polynomial(poly.head)

    def test_anti_derivative_with_non_numeric_val(self):
        poly = self.create_linked_list(["a", 2, 3])  # Non-numeric value
        with self.assertRaises(TypeError):
            self.calc.anti_derivative_polynomial(poly.head)

    def test_anti_derivative_with_single_term(self):
        poly = self.create_linked_list([5])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertIsNotNone(result)

    def test_anti_derivative_with_single_zero_term(self):
        poly = self.create_linked_list([0])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertIsNotNone(result)

    def test_anti_derivative_with_all_zero_terms(self):
        poly = self.create_linked_list([0, 0, 0])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertIsNotNone(result)

    def test_anti_derivative_with_alternating_signs(self):
        poly = self.create_linked_list([1, -2, 3, -4])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertIsNotNone(result)

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
