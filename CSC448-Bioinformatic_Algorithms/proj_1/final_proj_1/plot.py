# Importing Python packages
import scipy
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import seaborn as sns

# Reading the fasta file and keeping the formatted sequence's name and sequence
def file_reader(sequence_file):
    #create an empty sequence to put the values into it
    sequences = []
    #reads the file
    with open(sequence_file, 'r') as file:
        #for each line, strips and splits it into 3 variables
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                id1, id2, score = parts[0], parts[1], float(parts[2])
                #add them into the sequences to be used later
                sequences.append((id1,id2,score))
    return sequences           

def matrix_maker(converted_array):
    #gets the names and puts them into a list for the matrix
    names = list({id for results in converted_array for id in (results[0], results[1])})
    #sorts them just in case
    names.sort()
    #creates a matrix with the names for the columns and rows
    similarity_matrix = pd.DataFrame(1.0, index=names, columns=names)
    #for each distance, convert it into a similarity to make a similairty matrix
    for id1, id2, dist in converted_array:
        sim = 1 - dist
        similarity_matrix.loc[id1, id2] = sim
        similarity_matrix.loc[id2, id1] = sim
    #this fills all the diagonals with a 0 for the self aligned sequences    
    np.fill_diagonal(similarity_matrix.values, 0)     
    #print(similarity_matrix)
    return similarity_matrix

def find_seqeuences(matrix):
    #initialzes the min, max, closet,and farthest with default values
    min = float('inf')
    max = float('-inf')
    closest = None
    farthest = None
    #gets the names from the matix index
    names = matrix.index.tolist()
    #iterates through each in the matrix to find the min and max (closest and farthest) sequences
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            dist = matrix.iloc[i, j]
            if dist < min:
                min = dist
                closest = (names[i], names[j])
            if dist > max:
                max = dist
                farthest = (names[i], names[j])  
    #print them            
    print(f"\n Closest sequence is between {closest[0]} and {closest[1]} at distance {1- min:.4f}") 
    print(f"\n Farthest sequence is between {farthest[0]} and {farthest[1]} at distance {1- max:.4f}")                

def plot(similarity_matrix,num_clusters=3):
    #condenses the matrix into an array in order to plot
    condensed = scipy.spatial.distance.squareform(similarity_matrix.values)
    #method can either by averge, single, or complete
    linkage_matrix = linkage(condensed, method='average')
    #create an empty list to hold the silhouette scores
    sil_scores = []
    #tries clusters between 2-10
    range_n = range(2, 11)  


    for num_clusters in range_n:
        # generates cluster labels for the given number of clusters in the range
        cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')
        # calculates the silhouette score for each clustering
        score = silhouette_score(similarity_matrix.values, cluster_labels, metric='precomputed')
        #puts into the list
        sil_scores.append(score)
    #print(sil_scores)
        
    #prints and finds the max silhouette score which will tell us where its the best to cut the tree
    print(f"\nSilhouette score: {range_n[sil_scores.index(max(sil_scores))]}")

    #this prints the phylogenic tree
    plt.figure(figsize=(10, 6))
    dendrogram(linkage_matrix, labels=similarity_matrix.index.tolist(), leaf_rotation=90)
    plt.title("Phylogenetic Tree (Hierarchical Clustering)")
    plt.xlabel("Bacteria")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # reads the converted_scores.txt to be able to manipulate it
    file_1 = file_reader("converted_scores.txt")      

    #put the data into a matrix maker
    matrix = matrix_maker(file_1)
    #finds the closest and farthest sequences
    find_seqeuences(matrix)
    #plots the phylogenic tree
    plot_tree = plot(matrix)
