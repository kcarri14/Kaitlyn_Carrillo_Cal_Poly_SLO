import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialAntiDerivative(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def create_linked_list(self, coefficients):
        ll = LinkedList()
        for coeff in coefficients:
            ll.append(coeff)
        return ll

    def linked_list_to_list(self, head):
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def test_anti_derivative_simple_polynomial(self):
        poly = self.create_linked_list([3, 2, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0, 1.0, 1.0, 0])

    def test_anti_derivative_higher_degree_polynomial(self):
        poly = self.create_linked_list([4, 3, 2, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0, 1.0, 1.0, 1.0, 0])

    def test_anti_derivative_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-3, -2, -1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-1.0, -1.0, -1.0, 0])

    def test_anti_derivative_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([10, 20, 30])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [10/3, 10.0, 30.0, 0])

    def test_anti_derivative_polynomial_with_single_term(self):
        poly = self.create_linked_list([5])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [5.0, 0])

    def test_anti_derivative_polynomial_with_mixed_coefficients(self):
        poly = self.create_linked_list([-3, 4, -5, 6])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-3/4, 4/3, -5/2, 6.0, 0])

    def test_anti_derivative_polynomial_with_alternating_signs(self):
        poly = self.create_linked_list([1, -2, 3, -4])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/4, -2/3, 3/2, -4.0, 0])

    def test_anti_derivative_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([6, 5, 4, 3])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [6/4, 5/3, 2.0, 3.0, 0])

    def test_anti_derivative_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([1, 3, 5, 7])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/4, 1.0, 5/2, 7.0, 0])

    def test_anti_derivative_polynomial_with_constant_term(self):
        poly = self.create_linked_list([3, 0, 0])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0, 0.0, 0.0, 0.0])

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
