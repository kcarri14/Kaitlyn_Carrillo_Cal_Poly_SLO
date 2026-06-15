import sys
def binary_search(arr: list, start: int, finish: int):
    #checks if list is 1 or if the pointer are on the same index
    if start == finish:
        return arr[start]
    #finds the mid point in the list
    mid = (start + finish) // 2
    #recursively calls the function until its executed
    while start < finish:
        #checks if the right and left neighbors and also the two extremes are the same value as the mid
        if (mid == len(arr) - 1 or arr[mid] != arr[mid + 1]) and (mid == 0 or arr[mid] != arr[mid - 1]):
            return arr[mid]
        #checks if the index is even 
        if mid % 2 == 0:
            #if the index is even, sees if the right neighbor is the same value
            if arr[mid] == arr[mid + 1]:
                return binary_search(arr, mid + 2, finish) # searches right side of the list
            else: #if it is not the right neighbor, it must be the left
                return binary_search(arr, start, mid) #searches the left side of the list
        else:    
            #if the index is odd, see if the left neighbor is the same value
            if arr[mid] == arr[mid - 1]:
                return binary_search(arr, mid + 1, finish) #searches right side of the list
            else: #if it is not the left neighbor, it must be the right
                return binary_search(arr, start, mid -1) #searches left side of the list
           
def main():
    filename = sys.argv[1]
    with open(filename) as f:
        lines = f.readlines()
        L = [int(line.strip()) for line in lines if line.strip()]
        unique = binary_search(L,0, len(L)-1)
        print(unique)
if __name__ == '__main__':
    main()
