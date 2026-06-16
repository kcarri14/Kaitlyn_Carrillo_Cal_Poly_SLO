import random


#Modify the minheap class to be a priority queue. The data is not a list of tuples where the tuple is (value,playername,gold).
class MinHeap:
    def __init__(self):
        self.heap = []

    def enqueue(self, element):
        # Add the element to the end of the heap array
        self.heap.append(element)
        # Move the new element to its correct position to maintain the heap property
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        # Find the parent's index
        parent_index = (index - 1) // 2
        # If the new element is less than its parent, swap them and continue up the heap
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def dequeue(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        # Move the last element to the root and heapify down from the root
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index):
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        # Check if the left child exists and is smaller than the current smallest
        if left_child < len(self.heap) and self.heap[left_child] < self.heap[smallest]:
            smallest = left_child

        # Check if the right child exists and is smaller than the current smallest
        if right_child < len(self.heap) and self.heap[right_child] < self.heap[smallest]:
            smallest = right_child

        # If the smallest element is not the current element, swap and continue down the heap
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def play_turn(self):
        if self.heap == 0:
            return None
        dequeued = self.dequeue()
        roll = random.randint(1,6) + random.randint(1,6)
        dequeued = (roll, dequeued[1], dequeued[2] + roll)
        self.enqueue(dequeued)



        