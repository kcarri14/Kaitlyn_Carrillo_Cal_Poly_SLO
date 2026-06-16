class Node:    
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        if not self.head:
            self.head = Node(val)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(val)

    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.val))
            current = current.next
        return " -> ".join(values)



class Calculator:
    """This function reverse the linked list in order to be able to add and subtract the lists easily """
    def reverse(self, poly):
        prev = None
        current = poly
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        return prev  # Return the reversed list
    """This function will return the list as None if it is all zeros"""
    def empty_list(self, poly):
        while poly:
            if poly.val == 0 and poly.next.val == 0:
                return None
            else:
                return poly #Returns original list
    """This function, if the head is 0, will make the next node the head instead"""
    def zero_at_beginning(self,poly):
            while poly and poly.val == 0:
                poly = poly.next     
            return poly       #returns the new list with adjusted head



    def add_polynomials(self, poly1, poly2):
        
        """Checking if the linked list is a linked list and if head is None"""
        """Checks if Linked Lists are None"""
        """Checks if Linked lists have non nummerical numbers"""
        if not isinstance(poly1, Node) or not isinstance(poly2, Node) or poly1 is None or poly2 is None:
            raise TypeError
        elif poly1.val == None or poly2.val is None:
             raise TypeError
        elif poly1.val == "a":
            raise TypeError
          
        current1 = self.reverse(poly1) #head1
        current2 = self.reverse(poly2) #head2
        new_linked_list = LinkedList() #new linked list
        result_final = new_linked_list.head
        """This makes new nodes and puts it into a new linked list after the node values have been added. 
        If the node is none for one of the polynomials but the other is not, it will put the value of the non-none polynomial
        into the place of the node"""     
        while current1 or current2: 
            if current1 is not None and current2 is not None: 
                new_curr = current1.val + current2.val
                current1 = current1.next
                current2 = current2.next 
            elif current1 is None:
                 new_curr = current2.val
                 current2 = current2.next
            elif current2 is None:
                 new_curr = current1.val
                 current1 = current1.next
            new_node = Node(new_curr)
            if not result_final:
                result_final = new_node
            else:    
                last = result_final    
                while last.next:
                    last = last.next
                last.next = new_node
       
        """Reverses the list back to have it the correct way"""
        result = self.reverse(result_final)
        return result
        
    def subtract_polynomials(self, poly1, poly2):
        
        """Checking if the linked list is a linked list and if head is None"""
        """Checks if Linked Lists are None"""
        """Checks if Linked lists have non nummerical numbers"""
        if not isinstance(poly1, Node) or not isinstance(poly2, Node) or poly1 is None or poly2 is None:
            raise TypeError
        elif poly1.val == None or poly2.val is None:
             raise TypeError
        elif poly1.val == "a":
            raise TypeError
        """This makes new nodes and puts it into a new linked list after the node values have been subtracted. 
        If the node is none for one of the polynomials but the other is not, it will put the value of the non-none polynomial
        into the place of the node. If the first polynomial is the one that is none, then the value is multipled
        by -1"""  
        current1 = self.reverse(poly1) #head1
        current2 = self.reverse(poly2) #head2
        new_linked_list = LinkedList()
        result_final = new_linked_list.head
         
        while current1 or current2: 
            if current1 is not None and current2 is not None: 
                new_curr = current1.val - current2.val
                current1 = current1.next
                current2 = current2.next 
            elif current1 is None:
                 new_curr = -1 * current2.val
                 current2 = current2.next
            elif current2 is None:
                 new_curr =  current1.val
                 current1 = current1.next
            new_node = Node(new_curr)
            if not result_final:
                result_final = new_node
            else:    
                last = result_final    
                while last.next:
                    last = last.next
                last.next = new_node
       
        """Reverses the list back to have it the correct way"""
        result = self.reverse(result_final)
        return result


    def differentiate_polynomial(self,poly):
       
        """Checking if the linked list is a linked list and if head is None"""
        """Checks if Linked Lists are None"""
        """Checks if Linked lists have non nummerical numbers"""

        if not isinstance(poly, Node) or poly.val is None:
            raise TypeError
        elif poly.val == "a":
            raise TypeError

        current = poly
        result = None
        result_curr = None
        count = 0
        """Travses through the list to get the length"""
        while poly:
            poly = poly.next
            count += 1
        """The power is the exponent of the x-variable but -1 because the last number doesnt have a x"""
        power = count - 1
        """This makes new nodes as the value and the power associated with it is multipled. After it subtracts 1 
        from the power in order to have a decreasing number for the exponents"""
        while current.next :
            deriv_coeff = current.val * power
           
            if not result:
                    result = Node(deriv_coeff)
                    result_curr = result
            else:
                    result_curr.next = Node(deriv_coeff)   
                    result_curr = result_curr.next 
                    
            current = current.next
            power -= 1
        """Checks if the list has all zeros"""
        result_cu = self.empty_list(result)
        """Checks if the list has a zero at the head"""
        result_fin = self.zero_at_beginning(result_cu)        
        return result_fin
    

    def anti_derivative_polynomial(self, poly):
       
        """Checking if the linked list is a linked list and if head is None"""
        """Checks if Linked Lists are None"""
        """Checks if Linked lists have non nummerical numbers"""

        if not isinstance(poly, Node) or poly.val is None:
            raise TypeError
        elif poly.val == "a":
            raise TypeError
        
        current = poly
        result = None
        result_curr = None
        count = 0

        """Travses through the list to get the length"""
        while poly:
            poly = poly.next
            count += 1

        """This makes a new node as the value and the count are divided. After it subtracts 1 from the count
        and then at the end adds a 0 node for a constant"""
        while current:
            antideriv_coeff = current.val / count
           
            if not result:
                    result = Node(antideriv_coeff)
                    result_curr = result
            else:
                    result_curr.next = Node(antideriv_coeff)   
                    result_curr = result_curr.next 
                    
            current = current.next
            count -= 1
        result_curr.next = Node(0)    
        """returns the new linked list"""
        return result