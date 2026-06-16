import array

class MaxHeap:
    def __init__(self, size=0):
        self.heap = array.array('i', [0]*size)  # Initializes the heap with a predefined size for integers
        self.current_size = 0  # Tracks the current number of elements in the heap

    def heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] > self.heap[parent_index]:
                # Swap the current node with its parent if the heap property is violated
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def insert(self, element):
        if self.current_size < len(self.heap):
            # Replace the value at the current position if within the initial size
            self.heap[self.current_size] = element
        else:
            # Dynamically resize the heap array for new element insertion
            self.heap.append(element)
        self.heapify_up(self.current_size)
        self.current_size += 1

    def peek(self):
        if self.current_size > 0:
            return self.heap[0]
        else:
            raise Exception("Heap is empty")

    def heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < self.current_size and self.heap[left] > self.heap[largest]:
            largest = left

        if right < self.current_size and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self.heapify_down(largest)

    def extract_max(self):
        if self.current_size <= 0:
            raise Exception("Heap is empty")
        max_element = self.heap[0]
        self.heap[0] = self.heap[self.current_size - 1]
        self.current_size -= 1
        self.heapify_down(0)
        return max_element

# Initialize the heap with a predefined size (optional)
heap = MaxHeap(10)

# Insert elements into the heap
heap.insert(20)
heap.insert(15)
heap.insert(30)
heap.insert(40)

print("After inserting 20, 15, 30, 40:")
# Expected to show that the maximum (40) is at the root of the heap
for i in range(heap.current_size):
    print(heap.heap[i], end=' ')
print("\n")

# Peek at the maximum element without removing it
max_element_peek = heap.peek()
print(f"Peek at the maximum element: {max_element_peek}")
# Expected output: Peek at the maximum element: 40

# Extract the maximum element
max_element_extracted = heap.extract_max()
print(f"Maximum element extracted: {max_element_extracted}")
# Expected output: Maximum element extracted: 40

print("Heap after extracting the maximum element:")
for i in range(heap.current_size):
    print(heap.heap[i], end=' ')
print("\n")

# Insert another element and observe changes
heap.insert(50)
print("After inserting 50:")
for i in range(heap.current_size):
    print(heap.heap[i], end=' ')
print("\n")

# Peek and extract again to demonstrate heap operations
max_element_peek_again = heap.peek()
print(f"Peek at the maximum element again: {max_element_peek_again}")
# Expected output: Peek at the maximum element again: 50

max_element_extracted_again = heap.extract_max()
print(f"Maximum element extracted again: {max_element_extracted_again}")
# Expected output: Maximum element extracted again: 50

print("Final state of the heap:")
for i in range(heap.current_size):
    print(heap.heap[i], end=' ')


