
# Importing Python packages
from enum import IntEnum
import numpy as np
import blosum as bl
from itertools import combinations

#THIS IS FROM THE OUTSIDE IMPLEMENTATION OF SMITH WATERMAN ALGORITHM
# Assigning the constants for the scores
class Score(IntEnum):
    GAP = -12

# Assigning the constant values for the traceback
class Trace(IntEnum):
    STOP = 0
    LEFT = 1 
    UP = 2
    DIAGONAL = 3

#THIS IS FROM THE OUTSIDE IMPLEMENTATION OF SMITH WATERMAN ALGORITHM
# Reading the fasta file and keeping the formatted sequence's name and sequence
def fasta_reader(sequence_file):
    #creates list for the sequences 
    sequences = []
    #reads the file and adds each sequence into array
    with open(sequence_file, 'r') as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                sequences.append((parts[0], parts[1]))
    return sequences  
         
#I WROTE THIS FUNCTION BY MYSELF TO RUN ALL THE SMITH WATERMAN ALGORITHMS ON ALL THE COMBINATIONS
#takes in the sequence array from the reader and for all combination puts it through the smith waterman algorithm
def run_all_smith_waterman(sequences):
    #creates a results array to store the results of the smith waterman algorithm
    results = []
    for (id1, sequence1), (id2, sequence2) in combinations(sequences, 2):
        score = smith_waterman(sequence1, sequence2)
        results.append((id1,id2,score))
    #print(results)    
    return results, sequences    

#THIS IS FROM THE OUTSIDE IMPLEMENTATION OF SMITH WATERMAN ALGORITHM
# Implementing the Smith Waterman local alignment
def smith_waterman(seq1, seq2):
    # Generating the empty matrices for storing scores and tracing
    row = len(seq1) + 1
    col = len(seq2) + 1
    matrix = np.zeros(shape=(row, col), dtype=int)  
    tracing_matrix = np.zeros(shape=(row, col), dtype=int)  
    
    # Initialising the variables to find the highest scoring cell
    max_score = -1
    max_index = (-1, -1)
    
    # Calculating the scores for all cells in the matrix
    for i in range(1, row):
        for j in range(1, col):
           
            res1 = seq1[i-1]
            res2 = seq2[j-1]

            if res1 in blosum_matrix and res2 in blosum_matrix[res1]:
                match_value = blosum_matrix[res1][res2]
            else:
                match_value = -1

            diagonal_score = matrix[i - 1, j - 1] + match_value
            
            # Calculating the vertical gap score
            vertical_score = matrix[i - 1, j] + Score.GAP
            
            # Calculating the horizontal gap score
            horizontal_score = matrix[i, j - 1] + Score.GAP
            
            # Taking the highest score 
            matrix[i, j] = max(0, diagonal_score, vertical_score, horizontal_score)
            
            # Tracking where the cell's value is coming from    
            if matrix[i, j] == 0: 
                tracing_matrix[i, j] = Trace.STOP
                
            elif matrix[i, j] == horizontal_score: 
                tracing_matrix[i, j] = Trace.LEFT
                
            elif matrix[i, j] == vertical_score: 
                tracing_matrix[i, j] = Trace.UP
                
            elif matrix[i, j] == diagonal_score: 
                tracing_matrix[i, j] = Trace.DIAGONAL 
                
            # Tracking the cell with the maximum score
            if matrix[i, j] >= max_score:
                max_index = (i,j)
                max_score = matrix[i, j]
    
    # Initialising the variables for tracing
    aligned_seq1 = ""
    aligned_seq2 = ""   
    current_aligned_seq1 = ""   
    current_aligned_seq2 = ""  
    (max_i, max_j) = max_index
    
    # Tracing and computing the pathway with the local alignment
    while tracing_matrix[max_i, max_j] != Trace.STOP:
        if tracing_matrix[max_i, max_j] == Trace.DIAGONAL:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = seq2[max_j - 1]
            max_i = max_i - 1
            max_j = max_j - 1
            
        elif tracing_matrix[max_i, max_j] == Trace.UP:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = '-'
            max_i = max_i - 1    
            
        elif tracing_matrix[max_i, max_j] == Trace.LEFT:
            current_aligned_seq1 = '-'
            current_aligned_seq2 = seq2[max_j - 1]
            max_j = max_j - 1
            
        aligned_seq1 = aligned_seq1 + current_aligned_seq1
        aligned_seq2 = aligned_seq2 + current_aligned_seq2
    
    # Reversing the order of the sequences
    aligned_seq1 = aligned_seq1[::-1]
    aligned_seq2 = aligned_seq2[::-1]
    
    return max_score

def convert_scores(results, sequences):
    #creates a dictionary with the names from the sequences
    sequence_dict = {name: seq for name, seq in sequences}
    #creates a set for the results
    self_scores = {}
    #for each name in the dictionary, it calculates the self aligned scores for each sequence and places it into the set
    for name in sequence_dict:
        self_scores[name] = smith_waterman(sequence_dict[name], sequence_dict[name])
    #print(self_scores)

    #creates an empty list to have the converted scores
    converted_array = []

    #for each score, we are normalizing the score by taking the score from results and dividing it by the max of the self aligned scores
    for id1, id2, score in results:  
        converted = score / max(self_scores[id1], self_scores[id2])
        converted_array.append((id1, id2, converted))
    #print(converted_array)
    return converted_array

if __name__ == "__main__":
    #reads the file 
    file_1 = fasta_reader("data.txt")

    #BLOSUM62
    blosum_matrix = bl.BLOSUM(62)
    val = blosum_matrix["A"]["Y"]
    print(f"Score for A-Y: {val}")

    if len(file_1) >= 2:
        #run smith waterman on the file that was read
        output_2, sequences = run_all_smith_waterman(file_1)
        #converts the scores to the normalized score
        array = convert_scores(output_2, sequences)

        #takes the normalized score data and adds them to a file so you just have to run the sequence once to find all the data
        with open("converted_scores.txt", "w") as f:
            for row in array:
                f.write(" ".join(map(str, row)) + "\n")

        #takes the raw score and puts into a file
        #this is not really needed just wanted to see what would happen
        with open("scores.txt", "w") as f:
            for row in output_2:
                f.write(" ".join(map(str, row)) + "\n")        
