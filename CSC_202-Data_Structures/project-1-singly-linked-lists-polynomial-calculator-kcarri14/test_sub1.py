import unittest
from proj1 import LinkedList, Calculator


class TestPolynomialSubtraction(unittest.TestCase):
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

    def test_subtract_simple_polynomials(self):
        poly1 = self.create_linked_list([3, 2, 1])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [2, 0, -2])

    def test_subtract_polynomials_resulting_in_negative(self):
        poly1 = self.create_linked_list([2, 4, 6])
        poly2 = self.create_linked_list([3, 5, 7])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-1, -1, -1])

    def test_subtract_polynomials_with_higher_degree_first(self):
        poly1 = self.create_linked_list([5, 4, 3, 2])
        poly2 = self.create_linked_list([1, 1, 1])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [5, 3, 2, 1])

    def test_subtract_polynomials_with_higher_degree_second(self):
        poly1 = self.create_linked_list([1, 1, 1])
        poly2 = self.create_linked_list([5, 4, 3, 2])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-5, -3, -2, -1])

    def test_subtract_identical_polynomials(self):
        poly1 = self.create_linked_list([3, 5, 7])
        poly2 = self.create_linked_list([3, 5, 7])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0])

    def test_subtract_polynomials_with_negative_coefficients(self):
        poly1 = self.create_linked_list([-1, -2, -3])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-2, -4, -6])

    def test_subtract_polynomials_with_large_coefficients(self):
        poly1 = self.create_linked_list([100, 200, 300])
        poly2 = self.create_linked_list([10, 20, 30])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [90, 180, 270])

    def test_subtract_polynomials_with_mixed_coefficients(self):
        poly1 = self.create_linked_list([-3, 4, -5])
        poly2 = self.create_linked_list([6, -7, 8])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-9, 11, -13])

    def test_subtract_polynomials_with_alternating_signs(self):
        poly1 = self.create_linked_list([1, -2, 3, -4])
        poly2 = self.create_linked_list([-1, 2, -3, 4])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [2, -4, 6, -8])

    def test_subtract_polynomials_with_single_terms(self):
        poly1 = self.create_linked_list([9])
        poly2 = self.create_linked_list([6])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [3])

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
