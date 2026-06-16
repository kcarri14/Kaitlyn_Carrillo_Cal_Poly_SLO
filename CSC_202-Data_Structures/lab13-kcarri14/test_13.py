import unittest

from lab13 import HashTable

class TestHashTable(unittest.TestCase):
    def test_initialization(self):
        ht = HashTable(5)
        self.assertEqual(ht.capacity, 5)
        self.assertEqual(len(ht.table), 5)
        self.assertEqual(ht.size, 0)
    
    def test_simple_hash(self):
        ht = HashTable()
        # The ASCII sum of "abc" is 97 + 98 + 99 = 294
        self.assertEqual(ht.simple_hash("abc"), 294 % ht.capacity)
    
    def test_insert_and_search(self):
        ht = HashTable()
        ht.insert("key1", "value1")
        self.assertEqual(ht.search("key1"), "value1")
        # Test updating an existing key
        ht.insert("key1", "new_value")
        self.assertEqual(ht.search("key1"), "new_value")
        # Test size increment
        self.assertEqual(ht.size, 1)
    
    def test_delete(self):
        ht = HashTable()
        ht.insert("key1", "value1")
        ht.insert("key2", "value2")
        self.assertTrue(ht.delete("key1"))
        self.assertEqual(ht.search("key1"), None)
        self.assertFalse(ht.delete("key3"))  # Non-existent key
        self.assertEqual(ht.size, 1)
    
    def test_resize_and_load_factor(self):
        # Initialize a small hash table to trigger resizing quickly
        ht = HashTable(2)
        ht.insert("key1", "value1")
        ht.insert("key2", "value2")
        # This insert should trigger resizing
        ht.insert("key3", "value3")
        self.assertGreater(ht.capacity, 2)  # Ensure the capacity has increased
        # Ensure all items are still accessible after resizing
        self.assertEqual(ht.search("key1"), "value1")
        self.assertEqual(ht.search("key2"), "value2")
        self.assertEqual(ht.search("key3"), "value3")

if __name__ == "__main__":
    unittest.main()
