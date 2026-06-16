class LinkedListQueue:
    class Node:
        def __init__(self, value=None, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def enqueue(self, item):
        newNode = self.Node(item)
        if self.tail:
            self.tail.next = newNode
        self.tail = newNode
        if not self.head:
            self.head = newNode

    def dequeue(self):
        if self.isEmpty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

class LinkedListStack:
    class Node:
        def __init__(self, value=None, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.top = None

    def isEmpty(self):
        return self.top is None

    def push(self, item):
        newNode = self.Node(item, self.top)
        self.top = newNode

    def pop(self):
        if self.isEmpty():
            return None
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        if self.isEmpty():
            return None
        return self.top.value


def bottomUpBFS(root):
    if root is None:   #If tree is empty it will return a linked list queue
        return LinkedListQueue()
    #initailize a linked list stack and a linked list queue
    stack = LinkedListStack()
    queue = LinkedListQueue()
    #enqueue the root into the queue
    queue.enqueue(root)
    # the while loop performs the BFS traversal
    while not queue.isEmpty():
        #Dequeue the node from the front
        current_node = queue.dequeue()
        #Push the dequeued node into the stack
        stack.push(current_node.value)
        #Enqueues the right child then the left child
        if current_node.right: 
            queue.enqueue(current_node.right)
        if current_node.left:
            queue.enqueue(current_node.left)    
    #create a queue to hold the values in the reveresed form
    reversed_queue = LinkedListQueue()
    while not stack.isEmpty():
        reversed_queue.enqueue(stack.pop())  

    return reversed_queue


   