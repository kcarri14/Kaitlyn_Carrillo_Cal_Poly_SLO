import unittest
from proj3 import huffman_encoding

class TestHuffmanEncoding(unittest.TestCase):
    def test_hello(self):
        input_string = "hello"
        expected_encoded = "1111100010"
        expected_codes = {'l': '0', 'o': '10', 'e': '110', 'h': '111'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_calpoly(self):
        input_string = "calpoly"
        expected_encoded = "011010101111101000"
        expected_codes = {'l': '10', 'y': '00', 'a': '010', 'c': '011', 'o': '110', 'p': '111'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_abracadabra(self):
        input_string = "abracadabra"
        expected_encoded = "01101001110011110110100"
        expected_codes = {'a': '0', 'r': '10', 'b': '110', 'c': '1110', 'd': '1111'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_google(self):
        input_string = "google"
        expected_encoded = "110011101100"
        expected_codes = {'o': '0', 'g': '11', 'e': '100', 'l': '101'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_ABBA(self):
        input_string = "ABBA"
        expected_encoded = "0110"
        expected_codes = {'A': '0', 'B': '1'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_ABC(self):
        input_string = "ABC"
        expected_encoded = "10110"
        expected_codes = {'C': '0', 'A': '10', 'B': '11'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_racecar(self):
        input_string = "racecar"
        expected_encoded = "11011000100111"
        expected_codes = {'a': '01', 'c': '10', 'e': '00', 'r': '11'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_doodle(self):
        input_string = "doodle"
        expected_encoded = "100010111110"
        expected_codes = {'o': '0', 'd': '10', 'e': '110', 'l': '111'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_artists(self):
        input_string = "artists"
        expected_encoded = "0100011011101110"
        expected_codes = {'r': '00', 's': '10', 't': '11', 'a': '010', 'i': '011'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test_plplplplee(self):
        input_string = "plplplplee"
        expected_encoded = "0110110110111010"
        expected_codes = {'p': '0', 'e': '10', 'l': '11'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)


if __name__ == "__main__":
    unittest.main()
