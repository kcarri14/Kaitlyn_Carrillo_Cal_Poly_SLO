import timeit
import matplotlib.pyplot as plt
from lab3_p1 import generate_random_lists
import random

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

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def measure_sort_time(sort_function, arr):
    return timeit.timeit(lambda: sort_function(arr.copy()), number=1)

def plot_sort_times(generated_lists):
    selection_times = []
    insertion_times = []
    list_sizes = [len(lst) for lst in generated_lists]

    for lst in generated_lists:
        selection_times.append(measure_sort_time(selection_sort, lst))
        insertion_times.append(measure_sort_time(insertion_sort, lst))

    # Plotting of the map
    plt.figure(figsize=(10, 6))
    plt.plot(list_sizes, selection_times, color='blue', label='Selection Sort')
    plt.plot(list_sizes, insertion_times, color='red', label='Insertion Sort')
    plt.xlabel('Size of List (n)')
    plt.ylabel('Execution Time (Seconds)')
    plt.title('Execution Time for Sorting Algorithms')
    plt.legend()
    plt.show()

    return selection_times, insertion_times

# Using the generated_lists from the previous code snippet
plot_sort_times(generate_random_lists(num_lists, min_size, max_size, min_val, max_val))