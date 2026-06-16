import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialDifferentiation(unittest.TestCase):
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

    def test_differentiate_simple_polynomial(self):
        poly = self.create_linked_list([3, 2, 1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [6, 2])

    def test_differentiate_higher_degree_polynomial(self):
        poly = self.create_linked_list([4, 3, 2, 1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [12, 6, 2])

    def test_differentiate_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-3, -2, -1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-6, -2])

    def test_differentiate_polynomial_with_mixed_coefficients(self):
        poly = self.create_linked_list([-3, 4, -5, 6])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-9, 8, -5])

    def test_differentiate_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([10, 20, 30])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [20, 20])

    def test_differentiate_polynomial_with_single_non_zero_term(self):
        poly = self.create_linked_list([5])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([1, 2, 3, 4])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [3, 4, 3])

    def test_differentiate_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([4, 3, 2, 1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [12, 6, 2])

    def test_differentiate_polynomial_with_negatives(self):
        poly = self.create_linked_list([-1, -2, -3, -4])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-3, -4, -3])

    def test_differentiate_polynomial_with_floats(self):
        poly = self.create_linked_list([0.5, 0.7, 2.3, 1.0])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.5, 1.4, 2.3])


if __name__ == '__main__':
    unittest.main()
