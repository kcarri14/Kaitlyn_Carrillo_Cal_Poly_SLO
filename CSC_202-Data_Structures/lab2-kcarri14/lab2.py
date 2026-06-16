

def max_list_iter(int_list):
    if int_list == None:
        raise ValueError
    elif int_list == []:
        return None
    else:
        max = int_list[0]
        for i in range(len((int_list))):
            if int_list[i] > max:
                max = int_list[i]
        return max


def reverse_rec(int_list):
    if int_list == None:
        raise ValueError
    elif int_list == []:
        return []
    elif len(int_list) == 1:
        return int_list
    elif len(int_list) <= 3:
        int_list[0], int_list[-1] = int_list[-1], int_list[0]
        return int_list   
    else:
      min = int_list[0]
      int_list[0] = int_list[-1]
      int_list[-1] = min
      return [int_list[0]] + reverse_rec(int_list[1:-1]) + [int_list[-1]]



def bin_search(target, low, high, int_list):
    if int_list == None:
        raise ValueError
    elif target not in int_list:
        return None
    elif high >= low:
        mid = (high + low)//2
        if int_list[mid] == target:
            return mid
        elif int_list[mid] > target:
            return bin_search(target, low, mid - 1, int_list)    
        else:
            return bin_search(target, mid + 1, high, int_list)
    else:
        return -1        



import unittest
from lab2 import max_list_iter

class TestMaxListIter(unittest.TestCase):

    def test_max_normal(self):
        self.assertEqual(max_list_iter([1, 2, 3, 4, 5]), 5)

    def test_max_empty(self):
        self.assertIsNone(max_list_iter([]))

    def test_max_single_element(self):
        self.assertEqual(max_list_iter([4]), 4)

    def test_max_negative(self):
        self.assertEqual(max_list_iter([-3, -1, -2]), -1)

    def test_max_raises_value_error(self):
        with self.assertRaises(ValueError):
            max_list_iter(None)   

class TestReverseRec(unittest.TestCase):

    def test_reverse_normal(self):
        self.assertEqual(reverse_rec([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])

    def test_reverse_empty(self):
        self.assertEqual(reverse_rec([]), [])

    def test_reverse_single_element(self):
        self.assertEqual(reverse_rec([1]), [1])

    def test_reverse_negative(self):
        self.assertEqual(reverse_rec([-5, -4, -3]), [-3, -4, -5])

    def test_reverse_raises_value_error(self):
        with self.assertRaises(ValueError):
            reverse_rec(None)

    
        
class TestBinSearch(unittest.TestCase):

    def test_search_found(self):
        self.assertEqual(bin_search(4, 0, 4, [1, 2, 3, 4, 5]), 3)

    def test_search_not_found(self):
        self.assertIsNone(bin_search(6, 0, 4, [1, 2, 3, 4, 5]))

    def test_search_empty(self):
        self.assertIsNone(bin_search(1, 0, 0, []))

    def test_search_single_element(self):
        self.assertEqual(bin_search(1, 0, 0, [1]), 0)

    def test_search_raises_value_error(self):
        with self.assertRaises(ValueError):
            bin_search(1, 0, 1, None)     

  


if __name__ == '__main__':
    unittest.main()
