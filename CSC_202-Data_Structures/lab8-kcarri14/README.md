[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/hghLOwbD)
### Lab 8: Exploring Sorting Algorithms

#### Objectives
1. Understand the mechanisms of various sorting algorithms: Insertion Sort, Selection Sort, Bubble Sort, Counting Sort, Merge Sort, Quick Sort.

#### Prerequisites
- Basic knowledge of Python programming.
- Familiarity with the concept of sorting algorithms.

#### Materials and Resources
- Lecture notes on sorting algorithms.

#### Instructions

Let's use this list as our example:
\[ \text{List} = [34, 47, 32, 56, 29, 78, 23, 35, 12, 17] \]

#### Algorithms:
1. Insertion Sort
2. Selection Sort
3. Bubble Sort
4. Counting Sort
5. Merge Sort
6. Quick Sort (pivot as the last element)

### Instructions for Each Algorithm

#### 1. Insertion Sort
- Start from the second element.
- Compare with previous elements and insert it in the correct position among those already considered sorted.
- **Track each comparison and swap.**

#### 2. Selection Sort
- Find the minimum element in the array and swap it with the element in the first position, then move to the next position and repeat.
- **Track each comparison and swap.**

#### 3. Bubble Sort
- Repeatedly step through the list, compare adjacent elements, and swap them if they are in the wrong order.
- **Track each comparison and swap.**

#### 4. Counting Sort (Note: This is more about counting occurrences than comparisons and swaps)
- Count the number of elements for each distinct value.
- Use the count to place each element in its correct position.
- **Track the counts and the reconstruction of the sorted array.**

#### 5. Merge Sort
- Divide the list into the smallest unit (1 element), then compare each element with the adjacent list to sort and merge them into a sorted list.
- **Track comparisons and the merging process.**

#### 6. Quick Sort (Pivot as the last element)
- Choose the last element as the pivot, partition the array around the pivot, and recursively apply to subarrays.
- **Track comparisons, swaps, and the pivot's position.**

### Example Tracking Table for Insertion Sort

| Step | Current Array | Comparisons | Swaps |
|------|---------------|-------------|-------|
| 1    | [34, 47, 32, 56, 29, 78, 23, 35, 12, 17] | 0 | 0 |
| 2    | [34, 47, 32, 56, 29, 78, 23, 35, 12, 17] | 1 | 0 |
| ...  | ... | ... | ... |
| Final| [12, 17, 23, 29, 32, 34, 35, 47, 56, 78] | X | Y |

- **Comparisons:** Total times two elements were compared.
- **Swaps:** Total times two elements were swapped.

### Task
For each sorting algorithm, create a table similar to the one above. Start with the initial array and manually sort the list step by step, documenting the number of comparisons and swaps made at each step until the array is sorted.

###Use l = [3,9,1,4,3,1,5,8,5,2,6,4]

#### Reflection
- Discuss the efficiency of each algorithm based on the number of comparisons and swaps.
- Reflect on the process of each algorithm and its best, average, and worst-case scenarios.

### No Submission Required