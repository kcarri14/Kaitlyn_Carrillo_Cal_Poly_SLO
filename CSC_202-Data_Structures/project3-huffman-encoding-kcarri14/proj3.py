class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Add a comparison method for nodes
    def __lt__(self, other):
        # Primary comparison based on frequency
        if self.freq == other.freq:
            # Secondary comparison based on alphabetical order of character
            return self.char < other.char
        return self.freq < other.freq
    
    def __str__(self):
        # String representation of the Node
        return f"Node: {self.char}, Freq: {self.freq}"

class MinHeap:
    def __init__(self):
        self.heap = []

    def enqueue(self, element):
        self.heap.append(element)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        while index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def dequeue(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child

        if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0
    
    def __str__(self):
        return '\n'.join(str(node) for node in self.heap)




#Tasks below. 
        
def count_frequency(s):
    #Generate a dictionary that will be key: value pairs of
    # char:frequency 
    dict1 = {}
    for char in s:
        if char in dict1:
            dict1[char] += 1
        else:
          dict1[char] = 1      
    #return the dictionary     
    return dict1
    

def create_priority_queue(frequency):
    """
    Accepts a frequency dictionary and returns a priority queue filled with nodes.
    """
    #Given a dictionary of char:frequency pairs
    #iterate and enqueue onto the priority queue
    queue = MinHeap()
    for char,freq in frequency.items():
        child = Node(char,freq)
        queue.enqueue(child)  
    #print(queue)   
    return queue


def build_tree_from_queue(priority_queue):
    """
    Takes a priority queue and constructs the Huffman tree.
    """
    #While priority queue is not empty
    while not priority_queue.is_empty():
        #iteratively build the huffman tree by dequeing 2 nodes
        #left is the first dequeu
        left = priority_queue.dequeue()
        #if you dequeue and queue becomes empty, return left since that is the root
        if priority_queue.is_empty():
            return left
        #right is the second dequeue
        right = priority_queue.dequeue()
        #Create new node by merging left and right
        #char is the alphabetically first char between left and right
        if left.char < right.char:
            #add the frequerncies
            new_node = Node(left.char, left.freq + right.freq)
            new_node.left = left
            new_node.right = right
        else:
            new_node = Node(right.char, left.freq + right.freq)
            new_node.left = left
            new_node.right = right  
        #enque that new node    
        priority_queue.enqueue(new_node)   
    return priority_queue


def generate_codes(node, prefix="", code=None):
    #Traverse the tree to generate a huffman encoding
     # the huffman encoding will be a dictionary char:encoding pairs
    if code is None:
        code = {} 
    #if node is Node return None     
    if node is None:
        return None
    #if node has a char, then code[node.char] = prefix
    if node.char is not None:
        code[node.char] = prefix
    #recursively calls generate_codes on the left, with prefix + "0" and code
    generate_codes(node.left, prefix + '0', code)
    #recursively calls generate_codes on the right, with prefix + "1" and code
    generate_codes(node.right, prefix + '1', code)   
    #returns the code dictionary 
    return code

def encode(s, codes):
    #This is given to you  
    return ''.join(codes[char] for char in s)

def decode(encoded_string, root):
    #for decode accept the encoded string, and the root of the huffman tree and producce a decoded string
    empty_string = ""
    current = root
    #go char by char in the encoded string, each char representing a bit
    #you'll need to travese your tree

    for char in encoded_string:
         #if the bit is 0 go left,
            if char == '0':
                current = current.left
        #if the bit is 1 go right    
            elif char == '1':
                current = current.right
              
    # contin   ue until you reach a leaf node and concatinate that char to your decoded string
            if current.left is  None and current.right is None:
                empty_string += current.char       
                current = root  

    #return the new string         
    return empty_string



def huffman_encoding(s):
    #This will be your main function
    #get the freq dictionary for the string
    count = count_frequency(s)
    #get the priority queue from the freq dictionary
    queue = create_priority_queue(count)
    #get the root of your huffman tree given the pq
    tree = build_tree_from_queue(queue)
    #get your encodings dictionary from searching your tree 
    encodings = generate_codes(tree)
    #get your encoding string
    encoded = encode(s, encodings)
    #decode your string
    decoded = decode(encoded, tree)
    #return your encoded string, decoded string, and encoding dictionary
    return encoded, decoded, encodings



