import unittest
from proj1 import LinkedList, Calculator

class TestPolynomialSubtractionEdgeCases(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def create_linked_list(self, coefficients):
        ll = LinkedList()
        for coeff in coefficients:
            ll.append(coeff)
        return ll

    def test_subtract_non_linked_list(self):
        poly1 = [1, 2, 3]  # Not a linked list
        poly2 = self.create_linked_list([3, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1, poly2.head)

    def test_subtract_one_linked_list_one_not(self):
        poly1 = self.create_linked_list([1, 2, 3])
        poly2 = [3, 4, 5]  # Not a linked list
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1.head, poly2)

    def test_subtract_with_none_head(self):
        poly1 = None  # None head
        poly2 = self.create_linked_list([3, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1, poly2.head)

    def test_subtract_with_none_val(self):
        poly1 = self.create_linked_list([None, 2, 3])  # None value in node
        poly2 = self.create_linked_list([3, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1.head, poly2.head)

    def test_subtract_with_non_numeric_val(self):
        poly1 = self.create_linked_list(["a", 2, 3])  # Non-numeric value
        poly2 = self.create_linked_list([3, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1.head, poly2.head)

    def test_subtract_with_both_none_heads(self):
        poly1 = None
        poly2 = None
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1, poly2)

    def test_subtract_with_one_none_head(self):
        poly1 = self.create_linked_list([1, 2, 3])
        poly2 = None
        with self.assertRaises(TypeError):
            self.calc.subtract_polynomials(poly1.head, poly2)

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
