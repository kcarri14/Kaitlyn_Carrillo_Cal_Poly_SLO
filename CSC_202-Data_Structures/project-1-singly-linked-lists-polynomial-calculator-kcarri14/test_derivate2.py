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
        poly = self.create_linked_list([4, 0, 6])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [8, 0])

    def test_differentiate_higher_degree_polynomial(self):
        poly = self.create_linked_list([6, 0, 3, 0])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [18, 0, 3])

    def test_differentiate_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-5, -1, -8])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-10, -1])

    def test_differentiate_polynomial_with_single_term(self):
        poly = self.create_linked_list([-8])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([1, 7, 10, 40])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [3, 14, 10])

    def test_differentiate_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([14, 33, 28, 14])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [42, 66, 28])

    def test_differentiate_polynomial_with_alternating_signs(self):
        poly = self.create_linked_list([-1, 2, -2, 8])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-3, 4, -2])

    def test_differentiate_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([100, 200, 300])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [200, 200])

    def test_differentiate_polynomial_with_zero_and_non_zero_coefficients(self):
        poly = self.create_linked_list([0, 2, 0, 2])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [4, 0])

    def test_differentiate_polynomial_with_single_non_zero_term(self):
        poly = self.create_linked_list([0, 0, 3])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()
