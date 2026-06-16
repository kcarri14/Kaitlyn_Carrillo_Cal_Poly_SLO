import array
import random
class ArrayStack:
    def __init__(self, capacity):
        self.stack = array.array('i', [0] * capacity)
        self.top = -1
        self.capacity = capacity

    def push(self, item):
        if self.top < self.capacity -1:
            self.top += 1
            self.stack[self.top] = item
        else:
            raise Exception("Stack is full")    

    def pop(self):
        if self.top >= 0:
            item = self.stack[self.top]
            self.top -= 1
            return item
        else:
            raise Exception("Stack is empty")


    def peek(self):
        if self.is_empty():
            return None
        return self.stack[self.top]

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.capacity - 1

    def size(self):
        return self.top + 1

def reverse_stack(stack):
    temp_stack = ArrayStack(stack.capacity)
    while not stack.is_empty():
        temp_stack.push(stack.pop())
    return temp_stack


def process_card_stack(cardStack):
    if cardStack == None or not isinstance(cardStack, ArrayStack):
        raise TypeError
    expected_size = 13
    if cardStack.top != expected_size -1:
        raise ValueError
    
    solutionStack = ArrayStack(13)
    discardStack = ArrayStack(13)
    count = 1
    while True:
        while not cardStack.is_empty(): 

            if cardStack.peek() == count:
                solutionStack.push(cardStack.pop())
                count += 1
            else:
                discardStack.push(cardStack.pop())    

        while not discardStack.is_empty():        
            if discardStack.peek() == count:
                solutionStack.push(discardStack.pop())
                count += 1
            else:
                cardStack.push(discardStack.pop()) 
        if count > expected_size:
            break        

    return solutionStack


# Example usage

cards = [3, 6, 4, 1, 2, 5, 9, 8, 7, 10, 13, 12, 11]
random.shuffle(cards)
cardStack = ArrayStack(13)
for card in cards:  # Example card stack
    cardStack.push(card)
# Process and print the solution stack
result = process_card_stack(cardStack)
while not result.is_empty():
    print(result.pop(), end=' ')

