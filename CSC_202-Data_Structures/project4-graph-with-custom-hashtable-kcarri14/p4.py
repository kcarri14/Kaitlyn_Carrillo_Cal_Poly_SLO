class Hashtable:
    """A simple hashtable implementation using linear probing for collision resolution.

    Attributes:
        capacity (int): The maximum number of items that can be stored in the hashtable.
        table (list): The underlying data structure for storing items in the hashtable.
        size (int): The current number of items stored in the hashtable.
    """

    def __init__(self, capacity=12):
        """Initialize a new Hashtable instance.
        
        Args:
            capacity (int): The maximum capacity of the hashtable. Default is 12.
        """
        self.capacity = capacity
        self.table = [None for _ in range(capacity)]
        self.size = 0

    def hash(self, key):
        """Generate a hash value for a given key.

        Args:
            key (str): The key to hash. Must be a single character.

        Returns:
            int: The hash value of the key, determined by its ASCII value modulo the capacity.

        Raises:
            ValueError: If the key is not a single character.
        """
        if len(key) != 1:
            raise ValueError("Key must be a single character.")
        return ord(key) % self.capacity

    def insert(self, key, value):
        """Insert a key-value pair into the hashtable.

        Uses linear probing to resolve collisions. If the key already exists, its value is updated.

        Args:
            key (str): The key to insert. Must be a single character.
            value: The value associated with the key.

        Raises:
            Exception: If the hashtable is full and cannot accommodate more items.
        """
        hash_key = self.hash(key)
        orignial_hash = hash_key
        while self.table[hash_key] is not None:
            if self.table[hash_key][0] == key:
                self.table[hash_key] = (key, value)
                return 
            hash_key = (hash_key + 1) % self.capacity
            if hash_key == orignial_hash:
                raise Exception("Table is full")   
        self.table[hash_key] = (key, value)
        self.size += 1

    def get(self, key):
        """Retrieve the value associated with a given key.

        Args:
            key (str): The key whose value is to be retrieved.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        hash_key = self.hash(key)
        original_hash = hash_key
        full_loop = False
        while True:
            if self.table[hash_key] is None:
                if full_loop:
                    return None
                hash_key = (hash_key + 1) % self.capacity
                if hash_key == original_hash:
                    full_loop = True
                continue    
            if self.table[hash_key][0] == key:
                return self.table[hash_key][1]   
            hash_key = (hash_key + 1) % self.capacity
            if hash_key == original_hash:
                break
        return None    

    def delete(self, key):
        """Delete a key-value pair from the hashtable.

        Args:
            key (str): The key to be deleted.

        Returns:
            bool: True if the item was successfully deleted, False otherwise.
        """
        hash_key = self.hash(key)
        original_hash = hash_key
        full_loop = False
        while True:
            if self.table[hash_key] is None:
                if full_loop:
                    return None
                hash_key = (hash_key + 1) % self.capacity
                if hash_key == original_hash:
                    full_loop = True
                continue    
            if self.table[hash_key][0] == key:
                self.table[hash_key] = None
                self.size -= 1
                return True
            hash_key = (hash_key + 1) % self.capacity
            if hash_key == original_hash:
                break
        return False    

    def print(self):
        """Print the contents of the hashtable in a readable format."""
        print("Hashtable contents:")
        for index, item in enumerate(self.table):
            if item is not None:
                print(f"Index {index}: Vertex {item[0]}, Neighbors {item[1]}")
            else:
                print(f"Index {index}: Empty")


class Graph:
    """A simple undirected graph implementation using a custom hashtable for adjacency lists.

    Attributes:
        graph (Hashtable): The hashtable used to store the adjacency lists of the graph.
    """

    def __init__(self, vertices):
        """Initialize a new Graph instance.

        Args:
            vertices (int): The number of vertices in the graph, which determines the capacity of the hashtable.
        """
        self.graph = Hashtable(vertices)
    
    def add_edge(self, src, dest):
        """Add an edge between two vertices in the graph.

        This method ensures the graph remains undirected by adding an entry in both vertices' adjacency lists.

        Args:
            src (str): The source vertex.
            dest (str): The destination vertex.
        """
        src_neighbors = self.graph.get(src)

        if not src_neighbors:
            self.graph.insert(src, [dest])
        else:
            src_neighbors.append(dest)
            self.graph.insert(src, src_neighbors)

        dest_neighbors = self.graph.get(dest)

        if not dest_neighbors:
            self.graph.insert(dest, [src])
        else:
            dest_neighbors.append(src)
            self.graph.insert(dest, dest_neighbors)

    def dfs_traversal(self, start_vertex, visited=None):
        """Perform a depth-first search (DFS) traversal from a given start vertex.

        Args:
            start_vertex (str): The vertex from which the DFS traversal starts.
            visited (set, optional): A set of already visited vertices to avoid cycles. Defaults to None.

        Returns:
            set: A set of vertices that were visited during the DFS traversal.
        """
        if visited is None:
            visited = set()
        visited.add(start_vertex)  
        print(start_vertex)
        neighbors = self.graph.get(start_vertex)
        for neighbor in neighbors:
            if neighbor not in visited:
                self.dfs_traversal(neighbor, visited)
        return visited          


if __name__ == "__main__":
    graph = Graph(12)  # Example capacity
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('C', 'E')
    graph.add_edge('D', 'F')
    graph.add_edge('E', 'F')
    graph.add_edge('F', 'G')

    print("DFS Traversal starting from vertex 'A':")
    graph.dfs_traversal('A')
    print()  # Newline for better readability

    # Optionally, print the graph's contents
    print("\nGraph's adjacency list:")
    graph.graph.print()