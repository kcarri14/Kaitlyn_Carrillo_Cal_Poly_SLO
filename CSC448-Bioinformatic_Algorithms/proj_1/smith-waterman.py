
# Importing Python packages
from enum import IntEnum
import numpy as np
import blosum as bl
from itertools import combinations
import pandas as pd
import scipy
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns

# Assigning the constants for the scores
class Score(IntEnum):
    GAP = -12

# Assigning the constant values for the traceback
class Trace(IntEnum):
    STOP = 0
    LEFT = 1 
    UP = 2
    DIAGONAL = 3

# Reading the fasta file and keeping the formatted sequence's name and sequence
def fasta_reader(sequence_file):
    sequences = []
    with open(sequence_file, 'r') as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                sequences.append((parts[0], parts[1]))
    return sequences           

def run_all_smith_waterman(sequences):
    results = []

    for (id1, sequence1), (id2, sequence2) in combinations(sequences, 2):
        score = smith_waterman(sequence1, sequence2)
        results.append((id1,id2,score))
    #print(results)    
    return results, sequences    

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
    sequence_dict = {name: seq for name, seq in sequences}

    self_scores = {}
    for name in sequence_dict:
        self_scores[name] = smith_waterman(sequence_dict[name], sequence_dict[name])
    #print(self_scores)
    converted_array = []
    
    for id1, id2, score in results:  
        converted = score / max(self_scores[id1], self_scores[id2])
        converted_array.append((id1, id2, converted))
    #print(converted_array)
    return converted_array

def matrix_maker(converted_array):
    names = list({id for results in converted_array for id in (results[0], results[1])})
    names.sort()
    distance_matrix = pd.DataFrame(1.0, index=names, columns=names)
    for id1, id2, sim in converted_array:
        distance = 1 - sim
        distance_matrix.loc[id1, id2] = distance
        distance_matrix.loc[id2, id1] = distance
    np.fill_diagonal(distance_matrix.values, 0)     

    return distance_matrix

def find_seqeuences(matrix):
    min = float('inf')
    max = float('-inf')
    closest = None
    farthest = None
    names = matrix.index.tolist()
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            dist = matrix.iloc[i, j]
            if dist < min:
                min = dist
                closest = (names[i], names[j])
            if dist > max:
                max = dist
                farthest = (names[i], names[j])  
    print(f"\n Closest sequence is between {closest[0]} and {closest[1]} at distance {min:.4f}") 
    print(f"\n Farthest sequence is between {farthest[0]} and {farthest[1]} at distance {max:.4f}")                

def plot(distance_matrix,num_clusters=3):
    condensed = scipy.spatial.distance.squareform(distance_matrix.values)
    linkage_matrix = linkage(condensed, method='average')

    plt.figure(figsize=(10, 6))
    #dendrogram(linkage_matrix, labels=distance_matrix.index.tolist(), leaf_rotation=90)
    dendrogram(linkage_matrix, color_threshold=10)
    plt.title("Phylogenetic Tree (Hierarchical Clustering)")
    plt.xlabel("Bacteria")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.show()

    # Generate cluster labels
    cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')

    # Reduce to 2D for visualization
    pca = PCA(n_components=2)
    coords = pca.fit_transform(distance_matrix)

    # Plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=coords[:, 0], y=coords[:, 1], hue=cluster_labels, palette='tab10')
    for i, label in enumerate(distance_matrix.index):
        plt.text(coords[i, 0] + 0.02, coords[i, 1], label, fontsize=9)

    plt.title("Cluster Visualization (PCA Projection)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(title="Cluster")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Reading the two required fasta sequences
    
    file_1 = fasta_reader("data.txt")

    blosum_matrix = bl.BLOSUM(62)
    val = blosum_matrix["A"]["Y"]
    print(f"Score for A-Y: {val}")

    if len(file_1) >= 2:
        output_2, sequences = run_all_smith_waterman(file_1)
        array = convert_scores(output_2, sequences)

        with open("converted_scores.txt", "w") as f:
            for row in array:
                f.write(" ".join(map(str, row)) + "\n")

        with open("scores.txt", "w") as f:
            for row in output_2:
                f.write(" ".join(map(str, row)) + "\n")        

        matrix = matrix_maker(array)
        find_seqeuences(matrix)
        plot_tree = plot(matrix)
