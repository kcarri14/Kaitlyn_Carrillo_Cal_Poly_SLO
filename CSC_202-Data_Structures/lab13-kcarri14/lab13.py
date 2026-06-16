class HashTable:
    def __init__(self, capacity=10):
        #Task1: Define the constructor class for the HashTable
        self.capacity = capacity
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0


    
    def simple_hash(self, key):
        #Tasks2: Write the mathematical hash function that converts a key into an index integer
        new_key = str(key)
        hash_index = sum([ord(char) for char in new_key]) % self.capacity
        return hash_index
    
    def insert(self, key, value):
        #Task3: Write the insert function that with get the index of the key then input the value
        hash_key = self.simple_hash(key)
        if self.table[hash_key] == []:
            self.table[hash_key].append((key, value)) 
            self.size += 1
        else:
            for i,pair in enumerate(self.table[hash_key]):
                if pair[0] == key:
                    self.table[hash_key][i] =(key,value)
                    print()
       
        
        self.check_load_factor()

    def search(self, key):
        #Task4: Write the search function that with take the key and retrieve the value
        hash_key = self.simple_hash(key)
        bucket = self.table[hash_key]
        if bucket != []:
            for pair in bucket:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        #Task5: Delete the key from the hash table
        hash_key = self.simple_hash(key)
        for pair in self.table[hash_key]:
            if pair[0] == key:
                self.table[hash_key].remove(pair)
                self.size -= 1
                return True
            else:
                return False 
        
    
    def check_load_factor(self):
        """Check the current load factor and resize if necessary."""
        load_factor = self.size/ self.capacity
        if load_factor > 0.75:
            self.resize(self.capacity * 2)
   

    
    def resize(self, new_capacity):
        #Task6: Write the rehash function that will make a new table and rehash the old list contents to the new list
        old_table = self.table
        self.capacity = new_capacity
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for item in bucket:

                self.insert(item[0], item[1])



"""# Example usage
hash_table = HashTable()
hash_table.insert("key1", "value1")
hash_table.insert("key2", "value2")
hash_table.insert("key3", "value3")

print(hash_table.search("key1"))  # Output: "value1"
print(hash_table.search("key3"))  # Output: "value3"

hash_table.delete("key2")
print(hash_table.search("key2"))  # Output: None

# Demonstrating resize by surpassing the load factor threshold
for i in range(4, 20):
    hash_table.insert(f"key{i}", f"value{i}")

print("After resizing:")
hash_table.search("key19")  # Expected to find "value19" without performance degradation"""
