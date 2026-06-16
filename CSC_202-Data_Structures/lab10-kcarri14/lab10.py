import array

class MinHeap:
    def __init__(self, size=0):
        self.heap = array.array('i', [0]*size)  # Initializes the heap with a predefined size for integers
        self.current_size = 0  # Tracks the current number of elements in the heap

    def heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] < self.heap[parent_index]:
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
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
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < self.current_size and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < self.current_size and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.heap[smallest], self.heap[index] = self.heap[index], self.heap[smallest]
            self.heapify_down(smallest)

        pass

    def extract_min(self):  # Renamed from extract_max to extract_min
        if self.current_size <= 0:
            raise Exception("Heap is empty")
        min_element = self.heap[0]
        self.heap[0] = self.heap[self.current_size - 1]
        self.current_size -= 1
        self.heapify_down(0)
        return min_element
    
def heap_sort(arr):
    min_heap = MinHeap()
    for x in arr:
        min_heap.insert(x)
    result = []
    for _ in range(len(arr)):
        result.append(min_heap.extract_min())
    return result
