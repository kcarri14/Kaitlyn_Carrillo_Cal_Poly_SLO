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
    
    def linked_list_to_list(self, head):
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result
    

#Addition Tests
    def test_add_simple_polynomials(self):
        poly1 = self.create_linked_list([56, 243, 323])
        poly2 = self.create_linked_list([409, 512, 643])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [465, 755, 966])

    def test_add_different_length_polynomials(self):
        poly1 = self.create_linked_list([1, 3, 4])
        poly2 = self.create_linked_list([5, 6])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 8, 10])

    def test_add_polynomials_with_negative_coefficients(self):
        poly1 = self.create_linked_list([-5, -6, -7])
        poly2 = self.create_linked_list([5, 6, 7])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0])

    def test_add_polynomials_resulting_in_higher_degree(self):
        poly1 = self.create_linked_list([3, 4])
        poly2 = self.create_linked_list([1, 6, 3])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 9, 7])

    def test_add_polynomials_with_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 0, 0])
        poly2 = self.create_linked_list([10, 45, 34])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [10, 45, 34])

    def test_add_single_term_polynomials(self):
        poly1 = self.create_linked_list([87])
        poly2 = self.create_linked_list([23])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [110])

    def test_add_polynomials_with_alternating_signs(self):
        poly1 = self.create_linked_list([10, -20, 30, -40])
        poly2 = self.create_linked_list([-10, 20, -30, 40])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0, 0])

    def test_add_polynomials_second_longer_than_first(self):
        poly1 = self.create_linked_list([34, 41])
        poly2 = self.create_linked_list([1, 2, 3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 37, 45])

    def test_add_polynomials_first_longer_than_second(self):
        poly1 = self.create_linked_list([1, 2, 34, 41])
        poly2 = self.create_linked_list([3, 4])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [1, 2, 37, 45])

    def test_add_polynomials_with_mixed_zero_and_non_zero_coefficients(self):
        poly1 = self.create_linked_list([0, 43, 0, 52])
        poly2 = self.create_linked_list([26, 0, 30, 0])
        result = self.calc.add_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [26, 43, 30, 52])

    def test_add_non_linked_list(self):
        poly1 = [4, 5, 6]  # Not a linked list
        poly2 = self.create_linked_list([3, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.add_polynomials(poly1, poly2.head)

    def test_add_one_linked_list_one_not(self):
        poly1 = self.create_linked_list([1, 2, 3])
        poly2 = [43, 41, 54]  # Not a linked list
        with self.assertRaises(TypeError):
            self.calc.add_polynomials(poly1.head, poly2)

    def test_add_with_none_head(self):
        poly1 = None  # None head
        poly2 = self.create_linked_list([65, 87, 50])
        with self.assertRaises(TypeError):
            self.calc.add_polynomials(poly1, poly2.head)

    def test_add_with_none_val(self):
        poly1 = self.create_linked_list([None, 2, 3])  # None value in node
        poly2 = self.create_linked_list([None, 4, 5])
        with self.assertRaises(TypeError):
            self.calc.add_polynomials(poly1.head, poly2.head)   
#Anti-Derivative Tests
    def test_anti_derivative_simple_polynomial(self):
        poly = self.create_linked_list([3, 2, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0, 1.0, 1.0, 0])

    def test_anti_derivative_higher_degree_polynomial(self):
        poly = self.create_linked_list([6,5,4, 3, 2, 1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0,1.0,1.0, 1.0, 1.0, 1.0, 0])

    def test_anti_derivative_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-5,-4,-3, -2, -1])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-1.0,-1.0,-1.0, -1.0, -1.0, 0])

    def test_anti_derivative_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([100, 200, 300])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [100/3, 100.0, 300.0, 0])

    def test_anti_derivative_polynomial_with_single_term(self):
        poly = self.create_linked_list([498])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [498.0, 0])

    def test_anti_derivative_polynomial_with_mixed_coefficients(self):
        poly = self.create_linked_list([3, -4, 5, -6])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [3/4, -4/3, 5/2, -6.0, 0])

    def test_anti_derivative_polynomial_with_alternating_signs(self):
        poly = self.create_linked_list([10, -20, 30, -40])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [10/4, -20/3, 30/2, -40.0, 0])

    def test_anti_derivative_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([7, 5, 4, 3])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [7/4, 5/3, 2.0, 3.0, 0])

    def test_anti_derivative_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([1, 3, 6, 7])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1/4, 1.0, 3.0, 7.0, 0])

    def test_anti_derivative_polynomial_with_constant_term(self):
        poly = self.create_linked_list([4,0, 0, 0])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.0,0.0, 0.0, 0.0, 0.0])
    
    def test_anti_derivative_with_alternating_signs(self):
        poly = self.create_linked_list([10, -20, 30, -40])
        result = self.calc.anti_derivative_polynomial(poly.head)
        self.assertIsNotNone(result)    
#Derivative Tests
    def test_differentiate_simple_polynomial(self):
        poly = self.create_linked_list([4, 3, 1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [8, 3])

    def test_differentiate_higher_degree_polynomial(self):
        poly = self.create_linked_list([6, 4, 3, 1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [18, 8, 3])

    def test_differentiate_polynomial_with_negative_coefficients(self):
        poly = self.create_linked_list([-10, -20, -1])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-20, -20])

    def test_differentiate_polynomial_with_mixed_coefficients(self):
        poly = self.create_linked_list([-4, 7, -5, 6])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-12, 14, -5])

    def test_differentiate_polynomial_with_large_coefficients(self):
        poly = self.create_linked_list([15, 30, 40])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [30, 30])

    def test_differentiate_polynomial_with_single_non_zero_term(self):
        poly = self.create_linked_list([345])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertIsNone(result)

    def test_differentiate_polynomial_with_increasing_coefficients(self):
        poly = self.create_linked_list([14, 24, 34, 44])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [42, 48, 34])

    def test_differentiate_polynomial_with_decreasing_coefficients(self):
        poly = self.create_linked_list([41, 31, 21, 11])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [123, 62, 21])

    def test_differentiate_polynomial_with_negatives(self):
        poly = self.create_linked_list([-14, -24, -34, -44])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [-42, -48, -34])

    def test_differentiate_polynomial_with_floats(self):
        poly = self.create_linked_list([0.5, 0.8, 2.3, 1.0])
        result = self.calc.differentiate_polynomial(poly.head)
        self.assertEqual(self.linked_list_to_list(result), [1.5, 1.6, 2.3])

#Subtraction tests
    def test_subtract_simple_polynomials(self):
        poly1 = self.create_linked_list([4, 5, 6])
        poly2 = self.create_linked_list([6, 5, 4])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-2, 0, 2])

    def test_subtract_polynomials_resulting_in_negative(self):
        poly1 = self.create_linked_list([2, 4, 6])
        poly2 = self.create_linked_list([5, 14, 17])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-3, -10, -11])

    def test_subtract_polynomials_with_higher_degree_first(self):
        poly1 = self.create_linked_list([5, 14, 13, 12])
        poly2 = self.create_linked_list([1, 1, 1])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [5, 13, 12, 11])

    def test_subtract_polynomials_with_higher_degree_second(self):
        poly1 = self.create_linked_list([2, 2, 1])
        poly2 = self.create_linked_list([5, 4, 3, 2])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-5, -2, -1, -1])

    def test_subtract_identical_polynomials(self):
        poly1 = self.create_linked_list([34, 55, 67])
        poly2 = self.create_linked_list([34, 55, 67])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [0, 0, 0])

    def test_subtract_polynomials_with_negative_coefficients(self):
        poly1 = self.create_linked_list([-1, -2, -3])
        poly2 = self.create_linked_list([11, 21, 31])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-12, -23, -34])

    def test_subtract_polynomials_with_large_coefficients(self):
        poly1 = self.create_linked_list([110, 210, 310])
        poly2 = self.create_linked_list([10, 20, 30])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [100, 190, 280])

    def test_subtract_polynomials_with_mixed_coefficients(self):
        poly1 = self.create_linked_list([-31, 41, -51])
        poly2 = self.create_linked_list([6, -7, 8])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [-37, 48, -59])

    def test_subtract_polynomials_with_alternating_signs(self):
        poly1 = self.create_linked_list([10, -20, 30, -40])
        poly2 = self.create_linked_list([-10, 20, -30, 40])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [20, -40, 60, -80])

    def test_subtract_polynomials_with_single_terms(self):
        poly1 = self.create_linked_list([967])
        poly2 = self.create_linked_list([632])
        result = self.calc.subtract_polynomials(poly1.head, poly2.head)
        self.assertEqual(self.linked_list_to_list(result), [335])
# Add many More tests

if __name__ == '__main__':
    unittest.main()
