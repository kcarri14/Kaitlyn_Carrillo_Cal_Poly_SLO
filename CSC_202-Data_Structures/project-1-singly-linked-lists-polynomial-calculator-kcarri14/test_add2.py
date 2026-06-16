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
        poly1 = self.create_linked_list([3, 0, 1])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [4, 2, 4])

    def test_add_polynomials_with_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 0, 0])
        poly2 = self.create_linked_list([1, 2, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 3])

    def test_add_polynomials_with_negative_and_zero_coefficients(self):
        poly1 = self.create_linked_list([-1, 0, -3])
        poly2 = self.create_linked_list([1, 2, 0])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 2, -3])

    def test_add_single_term_polynomials(self): 
        poly1 = self.create_linked_list([7]) 
        poly2 = self.create_linked_list([0,0]) 
        result = self.calc.add_polynomials(poly1.head, poly2.head) 
        self.assertEqual(self.linked_list_to_list(result), [0,7]) 
        
    def test_add_polynomials_different_lengths(self): 
        poly1 = self.create_linked_list([2, 4]) 
        poly2 = self.create_linked_list([3, 0, 7]) 
        result = self.calc.add_polynomials(poly1.head, poly2.head) 
        self.assertEqual(self.linked_list_to_list(result), [3, 2, 11]) 

    def test_add_polynomials_with_alternating_signs(self):
        poly1 = self.create_linked_list([7, -1, 8, -5])
        poly2 = self.create_linked_list([-4, 5, -8, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [3, 4, 0, -2])

    def test_add_polynomials_with_large_coefficients(self):
        poly1 = self.create_linked_list([100, 200, 300])
        poly2 = self.create_linked_list([10, 20, 30])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [110, 220, 330])

    def test_add_polynomials_second_longer_than_first(self):
        poly1 = self.create_linked_list([5, 1])
        poly2 = self.create_linked_list([1, 1, 1, 1])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 1, 6, 2])

    def test_add_polynomials_first_longer_than_second(self):
        poly1 = self.create_linked_list([7, 6, 2, 1])
        poly2 = self.create_linked_list([3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [7, 6, 5, 5])

    def test_add_polynomials_with_mixed_zero_and_non_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 3, 0, 3])
        poly2 = self.create_linked_list([2, 0, 2, 0])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [2, 3, 2, 3])

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
