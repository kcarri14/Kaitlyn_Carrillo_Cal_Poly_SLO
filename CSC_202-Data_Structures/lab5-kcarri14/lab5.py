class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        """ Initializes an empty doubly linked list. """
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        new_node.prev = curr

    def __eq__(self, other):
        if not isinstance(other, DoublyLinkedList):
            return False
        curr_self = self.head
        curr_other = other.head
        while curr_self and curr_other:
            if curr_self.data != curr_other.data:
                return False
            curr_self = curr_self.next
            curr_other = curr_other.next
        return curr_self == curr_other

    def __getitem__(self, index):
        """
        Gets the data of the node at the specified index.

        Parameters:
            index: The index of the node.

        Returns:
            The data of the node at the specified index.

        Raises:
            TypeError: If the index is not an integer.
            ValueError: If the index is negative.
            IndexError: If the index is out of range of the list.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        if index < 0:
            raise IndexError("Index must be non-negative")
        curr = self.head
        for _ in range(index):
            if curr is None:
                raise IndexError("Index out of range")
            curr = curr.next
        if curr is None:
            raise IndexError("Index out of range")
        return curr.data

    def __setitem__(self, index, data):
        """
        Sets the data of the node at the specified index.

        Parameters:
            index: The index of the node where the data is to be set.
            data: The data to set at the specified index.

        Raises:
            TypeError: If the index is not an integer.
            ValueError: If the index is negative.
            IndexError: If the index is out of range of the list.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        if index < 0:
            raise IndexError("Index must be non-negative")
        curr = self.head
        for _ in range(index):
            if curr is None:
                raise IndexError("Index out of range")
            curr = curr.next
        if curr is None:
            raise IndexError("Index out of range")
        curr.data = data

    def __str__(self):
        """
        String representation of the doubly linked list.

        Returns:
            A string representing the list elements.
        """
        result = []
        curr = self.head
        while curr:
            result.append(str(curr.data))
            curr = curr.next
        return ' <-> '.join(result)
