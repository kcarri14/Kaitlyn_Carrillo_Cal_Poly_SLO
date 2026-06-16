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
        poly = self.create_linked_list([1, 1, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/3, 1/2, 1.0,0])

    def test_anti_derivative_higher_degree_polynomial(self):
        poly = self.create_linked_list([5, 1, 2, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [5/4, 1/3, 1.0, 1.0, 0])

    def test_anti_derivative_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-2, -2, -2])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-2/3, -1.0, -2.0, 0])

    def test_anti_derivative_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([100, 200, 300])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [100/3, 100, 300, 0])

    def test_anti_derivative_polynomial_with_single_term(self):
        poly = self.create_linked_list([-8])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-8.0, 0])

    def test_anti_derivative_polynomial_with_mixed_coefficients(self):
        poly = self.create_linked_list([-2, 1, -7, 2])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-1/2, 1/3, -7/2, 2, 0])

    def test_anti_derivative_polynomial_with_alternating_signs(self):
        poly = self.create_linked_list([1, -2, 3, -2])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/4, -2/3, 3/2, -2, 0])

    def test_anti_derivative_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([4, 0, 2, 0])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0, 0.0 , 1.0, 0.0, 0])

    def test_anti_derivative_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([1, 2, 6, 8])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/4, 2/3, 3.0, 8.0, 0])

    

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
