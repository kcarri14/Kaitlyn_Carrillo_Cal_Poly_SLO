"""Task1: complete the append method WITHOUT using a tail"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return ' -> '.join(result)


"""Task2: Give two lists combine them into one list"""


def combine_linked_lists(list1, list2):
    # Check if both arguments are LinkedList instances
    if not isinstance(list1, LinkedList) or not isinstance(list2, LinkedList):
        raise TypeError

    # If the first list is empty, return the second list
    if list1.head == None:
       return list2


    # If the second list is empty, return the first list
    if list2.head == None:
        return list1


    # Find the end of the first list
    current = list1.head
    while current.next:
        current = current.next

    # Link the end of the first list to the start of the second list
    current.next = list2.head

    #return the new list
    return list1

"""Task3: Complete the function to determine is a linked list is a palindrome """
def is_palindrome(llist):
    # Check if the linked list is None or empty
    if llist == None:
        return False
    elif llist.head == None:
        return False
    
   

    # Convert linked list to a Python list for easy comparison
    convert_list = []
    char = llist.head
    while char:
        convert_list.append(char)
        char = char.next
    """Task1: complete the append method WITHOUT using a tail"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return ' -> '.join(result)


"""Task2: Give two lists combine them into one list"""


def combine_linked_lists(list1, list2):
    # Check if both arguments are LinkedList instances
    if not isinstance(list1, LinkedList) or not isinstance(list2, LinkedList):
        raise TypeError

    # If the first list is empty, return the second list
    if list1.head == None:
       return list2


    # If the second list is empty, return the first list
    if list2.head == None:
        return list1


    # Find the end of the first list
    current = list1.head
    while current.next:
        current = current.next

    # Link the end of the first list to the start of the second list
    current.next = list2.head

    #return the new list
    return list1

"""Task3: Complete the function to determine is a linked list is a palindrome """
def is_palindrome(llist):
    # Check if the linked list is None or empty
    if llist == None:
        return False
    elif llist.head == None:
        return False
    
   

    # Convert linked list to a Python list for easy comparison
    convert_list = []
    char = llist.head
    while char:
        convert_list.append(char.data)
        char = char.next   
    
    # Check if the list is a palindrome    
    length = len(convert_list)
    for i in range(length //2):
        if convert_list[i] != convert_list[length -i-1]:
            return False
    return True    
  
    



 