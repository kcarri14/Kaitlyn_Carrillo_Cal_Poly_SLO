import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialAddition(unittest.TestCase):
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

    def test_add_simple_polynomials(self):
        poly1 = self.create_linked_list([1, 2, 3])
        poly2 = self.create_linked_list([4, 5, 6])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [5, 7, 9])

    def test_add_different_length_polynomials(self):
        poly1 = self.create_linked_list([2, 3, 4])
        poly2 = self.create_linked_list([5, 6])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [2, 8, 10])

    def test_add_polynomials_with_negative_coefficients(self):
        poly1 = self.create_linked_list([-1, -2, -3])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0])

    def test_add_polynomials_resulting_in_higher_degree(self):
        poly1 = self.create_linked_list([3, 4])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 5, 7])

    def test_add_polynomials_with_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 0, 0])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 3])

    def test_add_single_term_polynomials(self):
        poly1 = self.create_linked_list([5])
        poly2 = self.create_linked_list([6])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [11])

    def test_add_polynomials_with_alternating_signs(self):
        poly1 = self.create_linked_list([1, -2, 3, -4])
        poly2 = self.create_linked_list([-1, 2, -3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0, 0])

    def test_add_polynomials_second_longer_than_first(self):
        poly1 = self.create_linked_list([3, 4])
        poly2 = self.create_linked_list([1, 2, 3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 6, 8])

    def test_add_polynomials_first_longer_than_second(self):
        poly1 = self.create_linked_list([1, 2, 3, 4])
        poly2 = self.create_linked_list([3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 6, 8])

    def test_add_polynomials_with_mixed_zero_and_non_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 4, 0, 5])
        poly2 = self.create_linked_list([2, 0, 3, 0])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [2, 4, 3, 5])



# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
