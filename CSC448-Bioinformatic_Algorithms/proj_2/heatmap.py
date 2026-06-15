import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import  fcluster, linkage, dendrogram
from sklearn.metrics import silhouette_score
import seaborn as sns
import pandas as pd
from scipy.stats import hypergeom


def read_file(ratio_file):
    sequences = []
    name_sequences = []
    with open(ratio_file, 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split("\t")
            values = list(map(float, parts[3:10]))
            name_sequences.append(parts[1])
            sequences.append(values)           
    return np.array(sequences), name_sequences

 
def heatmap(data):
    #Plots the raw row data as a heatmap
    plt.figure(figsize=(10, 6))
    xticklabel= ["R1.Ratio","R2.Ratio",	"R3.Ratio",	"R4.Ratio",	"R5.Ratio",	"R6.Ratio",	"R7.Ratio"]
    sns.heatmap(data, cmap="inferno", annot=False, xticklabels=xticklabel, yticklabels=False, vmin=0, vmax=5)
    plt.title('Gene Expression Heatmap Not clustered')
    plt.tight_layout()
    plt.show()

    #cluster genes and find silhouette scores
    linkage_matrix = linkage(data, method='ward')
    sil_scores = []
    range_n = range(2, 100)  

    for num_clusters in range_n:
        # generates cluster labels for the given number of clusters in the range
        cluster_labels = fcluster(linkage_matrix, num_clusters, criterion='maxclust')
        # calculates the silhouette score for each clustering
        score = silhouette_score(data, cluster_labels)
        #puts into the list
        sil_scores.append(score)
    max_silhouette = range_n[sil_scores.index(max(sil_scores))]
    print(f"\nSilhouette score: {max_silhouette}")
    

    #plots the silhouette score graph
    plt.figure(figsize=(8, 6))
    plt.plot(range_n, sil_scores, marker='o', linestyle='-', color='b', label='Silhouette Score')
    plt.title('Silhouette Scores')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.show()

    #clustering genes dendrogram
    # plt.figure(figsize=(25, 6))
    # dendrogram(linkage_matrix, leaf_rotation=90)
    # plt.title("Hierarchical Clustering Dendrogram")
    # plt.xlabel("Gene")
    # plt.ylabel("Distance")
    # plt.show()

    #assign cluster labels
    cluster_labels_2 = fcluster(linkage_matrix, max_silhouette, criterion='maxclust')
    #add labels to dataframe
    scaled_df = pd.DataFrame(data)
    scaled_df["Cluster"] = cluster_labels_2
    sorted_df = scaled_df.sort_values("Cluster").drop(columns=["Cluster"])
    #plots clustered heatmap
    plt.figure(figsize=(25, 6))
    sns.heatmap(sorted_df, cmap="RdBu", xticklabels=xticklabel, vmin=0, vmax=5)
    plt.title(f"Clustered Gene Expression Heatmap ")
    plt.xlabel("Time Point")
    plt.ylabel("Genes")
    plt.show()
 
def clustering_metric(data, name_data):
    DF = pd.DataFrame(data)
    # log2 transform for all genes
    data_log2 = np.log2(DF)
    # compute median across time points for each gene
    row_medians = data_log2.median(axis=1)
    # subtract the log2's because we want to divde them
    log2_fc = data_log2.sub(row_medians, axis=0)
    # max absolute log2 fold change across time points
    median_list = log2_fc.abs().max(axis=1)
    #adds the names to the data after being transformed
    median_list.index = name_data
    #finds the top 230 genes
    top_genes = median_list.nlargest(230).index
    return top_genes

def jaccard(scientist_data, my_data):
    #turns data into sets to be used for the jaccard coefficient
    my_set = set(my_data)
    scientist_set = set(scientist_data)
    intersection = len(my_set.intersection(scientist_set))
    print(f"Intersection: {intersection}")
    union = len(my_set.union(scientist_set))
    print(f"Union: {union}")
    jaccard_number = intersection / union
    print(f"Jaccard: {jaccard_number}")
    #finds common genes between the two sets
    common_genes = my_set.intersection(scientist_set)
    common_gene_list = []
    for gene in sorted(common_genes):
        common_gene_list.append(gene)
    print(f"List of genes in common with scientist data: {common_gene_list}")    


def redo_clustering_heatmap(top230_data):
    #print(top230_data)
    sequences = []
    with open("diauxic_raw_ratios.txt", 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split("\t")
            values = list(parts[1:10])
            sequences.append(values) 
         
    #print(sequences)  
    filtered_data = [row for row in sequences if row[0] in top230_data]
    #print(filtered_data)
    top230_raw_data = []
    for line in filtered_data:
        parts = line[2:10]
        top230_raw_data.append(parts)
    #print(top230_raw_data) 
    return top230_raw_data

def p_value(total_population, total_green, sample_green, sample_size):
    #finds the exact p-value for the given data 
    p_exact = hypergeom.sf(sample_green-1, total_population, total_green, sample_size) 
    print(f"Exact p_value: {p_exact}")
    #runs a simulation of picking 50 balls in 
    X = 1000000
    population = np.array([1]*total_green + [0]*(total_population - total_green))
    np.random.seed(42)
    green_counts = []
    for _ in range(X):
        sample = np.random.choice(population, sample_size, replace=False)
        green_counts.append(np.sum(sample))
    # calculates the estimated p-value
    green_counts = np.array(green_counts)
    p_estimate = np.mean(green_counts >= sample_green)
    print(f"Estimated p_value: {p_estimate}")
    #plots the p-values over the simulations to see when it stablizes
    trial_sizes = np.arange(1000, X+1, 1000)
    p_estimates = [np.mean(green_counts[:t] >= sample_green) for t in trial_sizes]

    plt.plot(trial_sizes, p_estimates)
    plt.axhline(p_estimate, color='red', linestyle='--', label=f"Final Estimate: {p_estimate:.4f}")
    plt.xlabel("Number of Simulations")
    plt.ylabel("Estimated P-value")
    plt.title("Stability of Simulated P-Value")
    plt.grid(True)
    plt.legend()
    plt.show()

def purple_pair():
    #finds the pair of numbers that will give a p-value between 0.003 and 0.01
    Total_population = 6000  
    for n in range(30, 101):  
        for k in range(15, n+1):  
            purple_genes_total = 420  
            p_value = hypergeom.sf(k-1, Total_population, purple_genes_total, n)
            if 0.003 < p_value < 0.01:
                print(n,k,p_value)  
    print("all done")              

if __name__ == "__main__":
    #plots the raw data onto a heatmap
    data, name_data = read_file("diauxic_raw_ratios.txt")
    heatmap(data)
    #writes just the values into its own file without the names or header
    with open("data.txt", "w") as f:
        for row in data:
            f.write(" ".join(map(str, row)) + "\n")
    #uses the clustering matrix to find the top 230 genes in the data       
    median_list = clustering_metric(data, name_data)   
    #writes the top 230 genes into a file     
    with open("my_top230.txt", "w") as f:
        for row in median_list:
            f.write(str(row) + "\n")
    #takes both the scientist top 230 and my 230 data and finds the jaccard coefficent between them        
    scientist_data, scientist_name_data = read_file("230genes_log_expression.txt")
    jaccard(scientist_name_data, median_list)
    #takes the list of the top 230 genes and finds the raw data to be used in a heatmap later
    my_top230 = redo_clustering_heatmap(median_list)
    df = pd.DataFrame(my_top230).astype(float)        
    heatmap(df)
    #gives a list of just the names from the scienists 230 data
    sequences = []
    with open("230genes_log_expression.txt", 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split("\t")
            values = parts[1]
            sequences.append(values) 
    #print(sequences)       
    #takes the list and finds the raw data with the scientist top 230 names and plots a heatmap         
    top230_scientist = redo_clustering_heatmap(sequences) 
    df_scientist = pd.DataFrame(my_top230).astype(float)  
    heatmap(df_scientist)  


    #PART 2 Stats                 
    Total_population= 6000        
    Total_Green= 4260        
    Sample_size = 50           
    Observed_Green = 38   
    p_value(Total_population, Total_Green, Observed_Green, Sample_size) 
    #finds n and k for purple balls
    purple_pair()      
