import matplotlib.pyplot as plt
import random
# Generating several long lists of integers for the task

def generate_random_lists(num_lists, min_size, max_size, min_val, max_val):
    random_lists = []
    for _ in range(num_lists):
        size = random.randint(min_size, max_size)
        random_list = random.sample(range(min_val, max_val), size)
        random_list.sort()
        random_lists.append(random_list)
    return random_lists
    
# Parameters for list generation

num_lists = 50  # Number of lists to generate
min_size = 100  # Minimum size of each list
max_size = 1000  # Maximum size of each list
min_val = 1  # Minimum value in the lists
max_val = 10000  # Maximum value in the lists

# Generate the lists
generated_lists = generate_random_lists(num_lists, min_size, max_size, min_val, max_val)



def linear_search(lst, target):
    comparsion = 0
    for n in range(len(lst)):
        comparsion += 1
        if lst[n] == target: 
            return comparsion
    return comparsion
    

def binary_search(lst, target):
    low = 0
    high = len(lst) -1
    comparsion = 0

    while low <= high:
        mid = (low + high) // 2
        if mid == target:
            comparsion += 1
            return mid
        elif lst[mid] >= target:
            comparsion += 1
            low = mid + 1
        else:
            comparsion += 1
            low = mid - 1   

    return comparsion

def compare_search(example_list, target):
    
    # Making a copy of the list for binary search to avoid altering the original list
    list_copy = example_list.copy()

    # Performing linear search
    linear_search_comparisons = linear_search(example_list, target)

    # Making a copy of the list for binary search to avoid altering the original list
    binary_search_comparisons = binary_search(list_copy, target)

    return linear_search_comparisons, binary_search_comparisons, len(example_list)

def plot_comparisons():
    
    ls_comparisons = []  # Linear search comparisons
    bs_comparisons = []  # Binary search comparisons
    list_sizes = []  # Sizes of the lists

    #puts comparisons into lists 
    for example_list in generated_lists:
        target = random.choice(example_list)
        linear_search_comp, binary_search_comp, size = compare_search(example_list, target)
        ls_comparisons.append(linear_search_comp)
        bs_comparisons.append(binary_search_comp)
        list_sizes.append(size)


    # Plotting of the map
    plt.figure(figsize=(10, 6))
    plt.scatter(list_sizes, ls_comparisons, color='blue', label='Linear Search')
    plt.scatter(list_sizes, bs_comparisons, color='red', label='Binary Search')
    plt.xlabel('Size of List (n)')
    plt.ylabel('Number of Comparisons')
    plt.title('Comparisons: Linear Search vs. Binary Search')
    plt.legend()
    plt.show()
    #Return a list of differences linear and binary search
    


# Call the plotting function
plot_comparisons()


