[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/MkBugmsX)
# Project3: Huffman Encoding

## Overview
Project3 is an implementation of Huffman Encoding, a widely used method for data compression. This project includes a detailed exploration of the Huffman encoding process, from frequency counting to tree construction and binary encoding/decoding. Special emphasis is placed on the `Node` and `MinHeap` classes provided, which are pivotal in constructing the Huffman tree and managing the priority queue, respectively.

## Features
- **Frequency Counting:** Analyzes the frequency of each character in the input string.
- **Priority Queue:** Utilizes a MinHeap to maintain the characters sorted by their frequencies.
- **Huffman Tree Construction:** Builds a Huffman tree based on character frequencies.
- **Encoding and Decoding:** Generates binary codes for characters and decodes them back to the original string.

## Classes and Functions

### Node Class
- Represents a tree node with character and frequency attributes.
- Includes comparison methods for priority queue operations.

### MinHeap Class (Modified)

1. **Primary Priority - Frequency:** Nodes are compared primarily by their frequency value. The node with the lower frequency has higher priority in the queue. 

2. **Secondary Priority - Alphabetical Order:** When two nodes have equal frequencies (i.e., a tie in primary priority), their comparison falls back on the alphabetical order of the characters they represent.

#### Key Functionalities
- **Enqueue:** Adds a new node to the priority queue. The insertion respects the min-heap property, ensuring that the node is placed according to its priority determined by the frequency of the character it represents and, in the case of a frequency

### count_frequency
- Generates a frequency dictionary for the input string.

### create_priority_queue
- Converts the frequency dictionary into a priority queue using the `MinHeap` class.

### build_tree_from_queue
- Constructs the Huffman tree from the priority queue.

### generate_codes
- Traverses the Huffman tree to generate binary codes for each character.

### encode & decode
- Encodes a string into a binary sequence and decodes it back using the generated Huffman tree.

## Tasks

In Project3: Huffman Encoding, participants are expected to implement several functions that utilize the provided `Node` and `MinHeap` classes. These tasks form the core of the Huffman Encoding algorithm, guiding you through the process of frequency counting, priority queue management, tree construction, and the encoding/decoding mechanism. Below is a breakdown of each function and its expected implementation.

### 1. `count_frequency(s)`
- **Objective:** Generate a frequency dictionary from the input string `s`, mapping each character to its frequency of occurrence.
- **Input:** A string `s`.
- **Output:** A dictionary with characters as keys and their frequencies as values.

#### Steps

1. **Initialize an Empty Dictionary:** Start by creating an empty dictionary. This dictionary will eventually contain characters as keys and their frequencies as values.

2. **Iterate Over the Input String:** Go through each character in the input string one by one. For every character encountered, you will perform an update operation on the dictionary.

3. **Update Frequency Count:** For each character, check if it already exists as a key in the dictionary.
   - If the character is already a key, increment its value by 1. This means the character has been found another time.
   - If the character is not found in the dictionary, add it as a new key with the value of 1. This marks the first occurrence of the character.

4. **Return the Dictionary:** After iterating through all characters in the string, the dictionary will be fully populated with the correct frequency counts for each character. Return this dictionary as the output of the function.


### 2. `create_priority_queue(frequency)`
- **Objective:** Convert the frequency dictionary into a priority queue using the `MinHeap` class, with each character encapsulated in a `Node` along with its frequency.
- **Input:** A frequency dictionary.
- **Output:** A `MinHeap` instance filled with `Node` instances for each character.

#### Process Breakdown
1. **Initialization of MinHeap:** Create an instance of the `MinHeap` class. This will serve as your priority queue where the nodes will be stored and ordered based on their frequencies.

2. **Iteration over Frequency Dictionary:** Loop through each entry in the frequency dictionary. The dictionary contains characters as keys and their frequencies as values.

3. **Node Creation and Enqueuing:**
   - For each character-frequency pair in the dictionary, create a new instance of the `Node` class. This node will contain the character (`char`) and its frequency (`freq`) as properties.
   - Enqueue each `Node` into the `MinHeap`. The `enqueue` method of the `MinHeap` will ensure that the nodes are added to the heap in a way that maintains the heap's property, i.e., the node with the smallest frequency is always at the root, allowing for efficient access and removal.

4. **Return Priority Queue:** After all character-frequency pairs have been enqueued, the `MinHeap` instance, now acting as a priority queue filled with nodes, is returned. This priority queue is a crucial component for the next steps of the Huffman encoding process, particularly for building the Huffman tree.

### 3. `build_tree_from_queue(priority_queue)`
- **Objective:** Construct the Huffman tree from the priority queue. This involves repeatedly removing the two nodes with the lowest frequency from the queue, combining them into a new node, and inserting the new node back into the queue until only one node remains (the root of the Huffman tree).
- **Input:** A `MinHeap` instance acting as the priority queue.
- **Output:** The root `Node` of the Huffman tree.

#### Process Breakdown
1. **Loop Until Single Node Remains:**
   - The process begins by checking if the priority queue is not empty, indicating that there are still nodes to be processed for tree construction.
   
2. **Dequeue Two Nodes:**
   - In each iteration, remove the two nodes with the lowest frequency from the priority queue. These are considered the nodes to be combined in this step. The first node removed is the left child, and the second node removed is the right child in the tree structure being built.
   
3. **Check for Last Node:**
   - After dequeuing a node, check if the priority queue becomes empty. If it does, the last node dequeued is the root of the Huffman tree, and the construction process is complete. This node is then returned as the output.

4. **Create New Combined Node:**
   - If the priority queue is not empty after removing two nodes, create a new node. This new node's frequency is the sum of the frequencies of the two dequeued nodes, and its character attribute is set to the alphabetically first character between the two child nodes. This ensures that the tree maintains a consistent ordering for nodes with equal frequencies.
   
5. **Enqueue New Node:**
   - Enqueue the new combined node back into the priority queue. This step reinserts the combined node into the priority queue, maintaining the min-heap property where nodes are ordered based on their frequency, and effectively builds up the Huffman tree by iteratively combining nodes.

6. **Iterative Combination:**
   - Repeat this process of dequeuing two nodes, combining them, and re-enqueueing the result until only one node remains in the priority queue. This final node is the root of the constructed Huffman tree.


### 4. `generate_codes(node, prefix="", code={})`
- **Objective:** Traverse the Huffman tree to generate the binary codes for each character. The traversal should update the `code` dictionary with binary strings representing the path to each character.
- **Input:** The root `Node` of the Huffman tree.
- **Output:** A dictionary mapping each character to its Huffman code.

#### Process Breakdown
1. **Base Case - Node is None:**
   - If the current node is `None`, it indicates that the path has reached beyond the leaf nodes, and the function should return without making any changes. This is the base case for the recursion.

2. **Identify Character Nodes:**
   - Check if the current node contains a character (`node.char is not None`). If it does, it means the traversal has reached a leaf node, which represents a character in the Huffman tree.
   - Update the `code` dictionary, assigning the current `prefix` as the binary code for the character. The `prefix` represents the accumulated path of "0"s and "1"s from the root to this leaf node.

3. **Recursive Traversal:**
   - If the current node is not a leaf node, continue the traversal down the tree.
   - Recursively call `generate_codes` for the left child of the current node, appending "0" to the `prefix`. This indicates a move to the left in the tree, which is represented by a "0" in the binary code.
   - Similarly, recursively call `generate_codes` for the right child, appending "1" to the `prefix`. A move to the right is represented by a "1" in the binary code.

4. **Return the Code Dictionary:**
   - After the recursive calls complete—having traversed the entire tree and populated the `code` dictionary with binary codes for all characters—the function returns the `code` dictionary.

### 5. `encode(s, codes)`
- **Objective:** Encode a string using the provided Huffman codes.
- **Input:** The original string `s` and the Huffman `codes` dictionary.
- **Output:** The encoded string as a binary sequence.

### 6. `decode(encoded_string, root)`
- **Objective:** Decode a binary sequence back into the original string using the Huffman tree.
- **Input:** The encoded binary sequence and the root `Node` of the Huffman tree.
- **Output:** The decoded original string.

#### Process Breakdown
1. **Initialize Decoding Process:**
   - Start with an empty string for the decoded message. This string will be populated with characters identified during the traversal of the Huffman tree.

2. **Traverse for Each Bit:**
   - Iterate through each bit in the encoded binary sequence. Each bit represents a direction to move within the Huffman tree: "0" indicates a move to the left child, and "1" indicates a move to the right child.

3. **Tree Navigation:**
   - Begin the traversal from the root of the Huffman tree.
   - For each bit in the encoded string:
     - If the bit is "0", move to the left child of the current node.
     - If the bit is "1", move to the right child of the current node.

4. **Identify Characters:**
   - Continue the traversal until reaching a leaf node. Leaf nodes in the Huffman tree represent characters of the original string.
   - Upon reaching a leaf node, append the character (`char`) associated with that leaf node to the decoded message string.

5. **Reset After Each Character:**
   - After appending a character to the decoded message, reset the current position back to the root of the Huffman tree to start decoding the next sequence of bits.

6. **Complete Decoding:**
   - Repeat the process of traversal and character identification for the entire length of the encoded binary sequence until all bits have been processed and the original message has been reconstructed.


### 7. `huffman_encoding(s)`
- **Objective:** The main function that orchestrates the Huffman encoding process by calling the above functions in sequence to encode an input string and then decode it to verify the process.
- **Input:** A string `s`.
- **Output:** The encoded string, the decoded string (for verification), and the Huffman codes dictionary.

#### Process Breakdown
1. **Frequency Analysis:**
   - Begin by analyzing the input string `s` to determine the frequency of each character. This is achieved by calling the `count_frequency(s)` function, which returns a dictionary mapping each character in the string to its frequency of occurrence.

2. **Priority Queue Creation:**
   - With the frequency dictionary in hand, create a priority queue that organizes the characters based on their frequencies. This step is crucial for building the Huffman tree and is accomplished by invoking `create_priority_queue(frequency)`, which returns a `MinHeap` filled with `Node` objects for each character.

3. **Huffman Tree Construction:**
   - Construct the Huffman tree from the priority queue by calling `build_tree_from_queue(priority_queue)`. This function iteratively combines the nodes with the least frequencies into new nodes until a single node remains, representing the root of the Huffman tree.

4. **Code Generation:**
   - Generate the Huffman codes for each character by traversing the newly constructed Huffman tree. The `generate_codes(root)` function accomplishes this, returning a dictionary where each character is mapped to its corresponding binary code.

5. **Encoding the String:**
   - Encode the input string using the Huffman codes obtained in the previous step. This encoding translates each character of the input string into its binary code, resulting in a compressed binary string that represents the encoded data.

6. **Decoding for Verification:**
   - Decode the binary string back into its original text form to verify the accuracy of the Huffman encoding process. This is achieved through the `decode(encoded_string, root)` function, which utilizes the Huffman tree to interpret the binary sequence back into text.

7. **Output:**
   - The function returns a tuple containing the encoded binary string, the decoded string (for verification purposes), and the dictionary of Huffman codes. This output not only showcases the compression achieved through Huffman encoding but also ensures that the original data can be accurately reconstructed from the encoded data.


### 8. Testing and Validation
Participants are expected to generate their own test cases for each function, which may require implementing `__eq__` methods for the `Node` and `MinHeap` classes to compare objects directly. This will ensure that your implementations are robust and handle a variety of input scenarios.


## Testing
- Implement 2 custom test cases for each function.
- If needed : Extend the `Node` and `MinHeap` classes with `__eq__` methods to facilitate testing.
- `https://asecuritysite.com/calculators/huff`
- You can use the above link to generate test case examples




