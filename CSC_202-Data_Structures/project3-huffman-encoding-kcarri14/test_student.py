import unittest
from proj3 import huffman_encoding, count_frequency, create_priority_queue, build_tree_from_queue, generate_codes, encode, decode, MinHeap, Node

class TestHuffmanEncoding(unittest.TestCase):
    def test1(self):
        input_string = "carrillo"
        expected_encoded = "00100011110101010011"
        expected_codes = {'a': '000', 'c': '001', 'i': '010', 'o': '011', 'l': '10', 'r': '11'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)
        
    def test2(self):
        input_string = "kaitlyn"
        expected_encoded = "10001001111110100110"
        expected_codes = {'a': '010', 'k': '100', 'i': '011', 't': '111', 'l': '101', 'y': '00', 'n': '110'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)   

    def test1_count_frequency(self):
        input_string = "carrillo"
        expected = {'c': 1, 'a': 1, 'r': 2, 'i': 1, 'l': 2, 'o': 1}
        result = count_frequency(input_string)
        self.assertEqual(result, expected)

    def test2_count_frequency(self):
        input_string = "kaitlyn"
        expected = {'k': 1, 'a': 1, 'i': 1, 't': 1, 'l': 1, 'y': 1, 'n': 1}
        result = count_frequency(input_string)
        self.assertEqual(result, expected)

    def test1_create_priority_queue(self):
        frequency = {'c': 1, 'a': 1, 'r': 2, 'i': 1, 'l': 2, 'o': 1}
        queue = create_priority_queue(frequency)
        self.assertFalse(queue.is_empty())

    def test2_create_priority_queue(self):
        frequency = {'c': 1, 'a': 1, 'r': 2, 'i': 1, 'l': 2, 'o': 1}
        queue = create_priority_queue(frequency)    
        expected_order = [('a', 1), ('i', 1), ('l', 2)]
        dequeued_items = []
        while not queue.is_empty():
            dequeued_items.append((queue.dequeue().char, queue.dequeue().freq))
        self.assertEqual(dequeued_items, expected_order)

    def test1_build_tree_from_queue(self):
        priority_queue_3 = MinHeap()
        tree_3 = build_tree_from_queue(priority_queue_3)
        self.assertIsNotNone(tree_3)  

    def test2_build_tree_from_queue(self):
        priority_queue_1 = MinHeap()
        node_1 = Node('a', 5)
        priority_queue_1.enqueue(node_1)
        tree_1 = build_tree_from_queue(priority_queue_1)
        self.assertEqual(tree_1, node_1)       
           
    def test1_generate_codes(self):
        input_string = 'carrillo'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        result = generate_codes(tree)
        expected = {'a': '000', 'c': '001', 'i': '010', 'o': '011', 'l': '10', 'r': '11'}
        self.assertEqual(result, expected)

    def test2_generate_codes(self):
        input_string = 'kaitlyn'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        result = generate_codes(tree)
        expected = {'a': '010', 'y': '00', 'i': '011', 'k': '100', 'l': '101', 'n': '110', 't': '111'}
        self.assertEqual(result, expected)   

    def test1_encode(self):
        input_string = 'carrillo'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        encodings = generate_codes(tree)    
        result = encode(input_string, encodings)
        expected = "00100011110101010011"
        self.assertEqual(result, expected)

    def test2_encode(self):
        input_string = 'kaitlyn'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        encodings = generate_codes(tree)    
        result = encode(input_string, encodings)
        expected = "10001001111110100110"
        self.assertEqual(result, expected)

    def test1_decode(self):
        input_string = 'carrillo'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        encodings = generate_codes(tree)    
        code = encode(input_string, encodings) 
        result = decode(code, tree)
        expected = "carrillo"
        self.assertEqual(result, expected)  

    def test2_decode(self):
        input_string = 'kaitlyn'
        count = count_frequency(input_string)
        queue = create_priority_queue(count)
        tree = build_tree_from_queue(queue)
        encodings = generate_codes(tree)    
        code = encode(input_string, encodings) 
        result = decode(code, tree)
        expected = "kaitlyn"
        self.assertEqual(result, expected)      
        

if __name__ == "__main__":
    unittest.main()        