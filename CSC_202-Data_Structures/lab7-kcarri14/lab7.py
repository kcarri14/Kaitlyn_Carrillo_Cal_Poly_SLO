"""Task1: Complete the implementation details for enqueue and dequeue"""

class Node:
    """A Node in a linked list."""
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedListQueue:
    """A Queue implementation using a linked list."""
    def __init__(self):
        self.front = self.rear = None

    def is_empty(self):
        """Check if the queue is empty."""
        return self.front is None

    def enqueue(self, value):
       new_node = Node(value)
       if self.rear is not None:
           self.rear.next = new_node
       self.rear = new_node 
       if self.front is None:
           self.front = new_node   
    def dequeue(self):
        if self.is_empty():
            return None
        value = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.tail = None
        return value    
    def peek_front(self):
        if self.is_empty():
            return None
        return self.front.value

    def to_list(self):
        """Convert the queue to a list for easy viewing."""
        elements = []
        current = self.front
        while current:
            elements.append(current.value)
            current = current.next
        return elements[::-1]

def sort_linked_list_queue_correctly(queue):
    sorted_queue = LinkedListQueue()
    count = 1
    while not queue.is_empty():
        num = queue.dequeue()
        if num == count:
            sorted_queue.enqueue(num)
            count += 1
        else:
            queue.enqueue(num)    
    return sorted_queue

# Create a linked list queue and add elements
#use this for debugging purposes

import random
queue = LinkedListQueue()
cards = [1,2,3,4,5,6,7,8,9,10,11,12,13]
random.shuffle(cards)
for card in cards:
    queue.enqueue(card)

# Sort the queue using the corrected method
sorted_queue_correctly = sort_linked_list_queue_correctly(queue)
print(sorted_queue_correctly.to_list()) # Convert the sorted queue to a list for display

"""Task4: No Submission for this task. What is the time complexity of your solution?"""
#The time complexity of my solution O(n)

