#Kaitlyn Carrillo Assignment 3

import numpy as np 
import networkx as nx
from itertools import combinations
import random
import matplotlib.pyplot as plt
import heapq
import pandas as pd
from scipy.stats import spearmanr


#needed for the dijkstra's algorithm
class Min_Heap:
    def __init__(self):
        self.heap = []

    def enqueue(self, item):
        heapq.heappush(self.heap, item)

    def dequeue(self):
        return heapq.heappop(self.heap)

    def isEmpty(self):
        return len(self.heap) == 0

#makes a graph
def graph():
    graph = nx.Graph()

    with open("interacting_proteins.txt", "r") as file:
        for line in file:
            node_1, node_2 = line.strip().split()
            graph.add_edge(node_1, node_2)
    return graph   

#IMPLEMENTED FROM CSC 202 CLASS
def dijkstra(graph, start):
    # Initialize distances from start to all other nodes as infinity
    distances = {vertex: float('infinity') for vertex in graph}
    # Distance from start to itself is 0
    distances[start] = 0
    # Priority queue: stores vertices and their current distances from start
    pq = Min_Heap()
    pq.enqueue((0, start))
    
    # Parent dictionary for path reconstruction
    parents = {vertex: None for vertex in graph}
    parents[start] = start

    while not pq.isEmpty():
        # Get the nearest unvisited node
        current_distance, current_vertex = pq.dequeue()
   
        # Explore neighbors
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + 1
            
            # If a shorter path to neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_vertex
                pq.enqueue((distance, neighbor))
    
    return distances

#finds average shortest path using dijkstra's
def average_shortest_path(graph, gene_list):
    total = 0
    count = 0
    for i, j in combinations(gene_list, 2): 
        distances = dijkstra(graph, i)
        if j in distances and distances[j] != float('infinity'):
            total += distances[j]
            count += 1
    return total / count if count > 0 else float('inf')

# does the random walk with restart algorithm 
def rwr(tran_matrix, start_index, gamma, probability_limit, max_iteration):
    #gets the shape like indexes of the matrix
    shape_tran_matrix = tran_matrix.shape[0]
    #makes a separate matrix with the same shape
    tracker_matrix = np.zeros(shape_tran_matrix)
    #makes the starter node 1
    tracker_matrix[start_index] = 1
    #restart matrix
    restart_matrix = np.eye(shape_tran_matrix)[start_index]
    #runs the rwr equation for the max_iteration times or until convergence
    for step in range(max_iteration):
        new_tracker_matrix = (1 - gamma) * np.dot(tran_matrix, tracker_matrix) + gamma * restart_matrix
        #checks for convergence
        if np.linalg.norm(new_tracker_matrix - tracker_matrix, 1) < probability_limit:
            return new_tracker_matrix, step + 1  # return steps used
        #update tracker
        tracker_matrix = new_tracker_matrix
    return tracker_matrix, max_iteration   

#does the spearman correlation calulcation using scipy
def spearman(node_rank_list, rwr_scores):
    correlation, p_val = spearmanr(node_rank_list, rwr_scores)
    return correlation, p_val

#finds the average random with restart
def average_rwr(transition_matrix, gene_set, gamma, convergence, max_iteration):
    all_scores = []
    steps_to_converge = []
    count = 0

    for gene in gene_set:
        if gene not in node_index:
            continue
        seed_index = node_index[gene]
        stationary, steps = rwr(transition_matrix, seed_index, gamma, convergence, max_iteration)
        sum_frequency = np.sum(stationary)
        if np.isclose(sum_frequency, 1.0, atol=1e-6):
            count += 1
        steps_to_converge.append(steps)

        scores = [
            stationary[node_index[g]]
            for g in gene_set
            if g != gene and g in node_index
        ]
        all_scores.extend(scores)

    avg_rwr_score = np.mean(all_scores) if all_scores else 0
    return avg_rwr_score, steps_to_converge, count

#random walk with restart with a different seed indices
def rwr_predict(transition_matrix, seed_indices, gamma, convergence, max_iteration):
    predict_matrix = transition_matrix.shape[0]
    restart_matrix = np.zeros(predict_matrix)
    restart_matrix[seed_indices] = 1/7
    restart_vector = restart_matrix.copy()

    for _ in range(max_iteration):
        new_restart = (1 - gamma) * np.dot(transition_matrix, restart_matrix) + gamma * restart_vector
        if np.linalg.norm(new_restart - restart_matrix, 1) < convergence:
            break
        restart_matrix = new_restart

    return restart_matrix
        


if __name__ == "__main__":
    edges = []
    #takes in the interacting protein file and puts the nodes into a set of proteins and edges to be used later
    with open("interacting_proteins.txt", "r") as file:
        for line in file:
            node_1, node_2 = line.strip().split()
            edges.append((node_1, node_2))
    #print(edges)
    networkx_graph = graph()

    #MAKES THE GRAPH

    # pos = nx.kamada_kawai_layout(networkx_graph)  

    # plt.figure(figsize=(12, 6))
    # nx.draw_networkx_nodes(networkx_graph, pos, node_size=2, node_color='skyblue', edgecolors='black')
    # nx.draw_networkx_edges(networkx_graph, pos, alpha=0.2, width=0.9)

    # plt.axis('off')
    # plt.title("Protein-Protein Interaction Graph with all genes")
    # plt.show()

    
    with open("onco_genes.txt", "r") as file:
        tumorgenic_genes = [gene.strip() for gene in file]
    #print(tumorgenic_genes)
    
    all_genes = list(networkx_graph.nodes())
    genes_without_tumor = []

    
    for genes in all_genes:
        if genes not in tumorgenic_genes:
            genes_without_tumor.append(genes)

    with open("data.txt", "w") as f:
        for row in genes_without_tumor:
            f.write(str(row) + "\n")
                    
    score_custom = average_shortest_path(networkx_graph, tumorgenic_genes)
    #print(score_custom)

    background_scores_custom = []

    for _ in range(1000):
        random_gene_sequences = random.sample(genes_without_tumor, 7)
        scores = average_shortest_path(networkx_graph, random_gene_sequences)   
        background_scores_custom.append(scores)
    #print(background_scores_custom)
    
    # plt.hist(background_scores_custom, edgecolor='black', bins=50)   
    # plt.axvline(score_custom, color='red')
    # plt.xlabel("Average Shortest Path")
    # plt.ylabel("Frequency")  
    # plt.show()  

    p_value = np.sum(np.array(background_scores_custom) <= score_custom) / 1000
    print("p-value of average shortest path(less):", p_value) 
    p_value_greater = np.sum(np.array(background_scores_custom) >= score_custom) / 1000
    print("p-value of average shortest path(less(greater)):", p_value_greater) 

    # make graph from picture
    toy_graph = nx.Graph()
    #add the edges to the graph
    edges = [("A", "B"),("A", "C"),("A", "H"),("A", "J"),("A", "K"),("B", "C"),("B", "D"),
             ("C", "E"),("D", "F"),("E", "G"),("F", "G"),("H", "I"),("I", "J") ]
    toy_graph.add_edges_from(edges)
    
    toy_graph_with_weights = nx.Graph()

    edges_with_weights = [("A", "B", 4.0),("A", "C", 4.0),("A", "H", 4.0),("A", "J", 4.0),("A", "K", 1.0),("B", "C", 1.0),("B", "D", 1.0),
             ("C", "E", 1.0),("D", "F", 1.0),("E", "G", 1.0),("F", "G", 1.0),("H", "I", 1.0),("I", "J", 1.0) ]

    toy_graph_with_weights.add_weighted_edges_from(edges_with_weights)

    graph = nx.Graph()

    with open("interacting_proteins.txt", "r") as file:
        for line in file:
            node_1, node_2 = line.strip().split()
            graph.add_edge(node_1, node_2)
    

    #makes an ajdaceny matrix from the graph
    nodes = list(graph.nodes())
    node_index = {node: i for i, node in enumerate(nodes)}
    length_nodes = len(nodes)
    adjacency_matrix = nx.adjacency_matrix(graph, nodes)

    #create the transition matrix from the adjacency matrix to put into the rwr function
    sum_columns = adjacency_matrix.sum(axis = 0)
    sum_columns[sum_columns == 0] = 1
    transition_matrix = (adjacency_matrix / sum_columns).toarray()

    #say what the start node is and run the rwr on it
    start_node = "A"
    start_index = node_index[start_node]
    stationary_frequency = rwr(transition_matrix, start_index, 0, 1e-6, 100000)

    #sums up the frequency to make sure that they are equal to 1
    sum_frequency = np.sum(stationary_frequency)
    print(sum_frequency)

    #creates a dictionary of the node and their value
    stationary_frequency_dict = {node: stationary_frequency[i] for node, i in node_index.items()}

    #puts them into two files so i can put it into cytpscape to make graph
    with open("ppi_network.edgelist_weights", "w") as f:
        f.write("source target\n")  # header
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")

    rwr_scores_file = pd.DataFrame({
        "gene": list(stationary_frequency_dict.keys()),
        "RWR_score": list(stationary_frequency_dict.values())
    })
    rwr_scores_file.to_csv("rwr_scores_weights_1.csv", index=False)

    rwr_score = list(stationary_frequency_dict.values())
    rank = [5, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1]

    core, p = spearman(rank, rwr_score)
    print(core)
    print(p)

    #finds the average rwr for the tumorigenic genes
    average_stationary_feq, average_steps, count_tumor = average_rwr(transition_matrix, tumorgenic_genes, 0.3, 1e-6, 100000)
    print(average_stationary_feq)
    print(average_steps)
    print(count_tumor)

    
    #random set for the background distrubtion of the rwr scores
    background_scores_rwr = []
    background_steps = []
    count_background_ = 0
    np.random.seed(56)

    for _ in range(1000):
        random_gene_sequences_rwr = random.sample(genes_without_tumor, 7)
        scores, average_steps_background, count_background = average_rwr(transition_matrix, random_gene_sequences_rwr, 0.3, 1e-6, 100000)   
        background_scores_rwr.append(scores)
        background_steps.append(average_steps_background)
#makes sure that each rwr iteration is summing up to 1         
        if np.isclose(count_background, 7.0, atol=1e-6):
            count_background_ += 1
    print(count_background_)        

    #writes the scores for each background set that was tested into a file
    with open("background_scores.txt", "w") as f:
        for u in background_scores_rwr:
            f.write(f"{u}\n")

    #write how many steps it takes to get to convergence for the background distrubtion into a file
    with open("background_steps.txt", "w") as f:
        for u in background_steps:
            f.write(f"{u}\n")        
    
    #p-value for the rwr based on the background scores
    p_value_less = np.sum(np.array(background_scores_rwr) <= average_stationary_feq) / 1000
    p_value_greater = np.sum(np.array(background_scores_rwr) >= average_stationary_feq) / 1000
    print("p-value less of rwr:", p_value_less)   
    print("p-value great of rwr:", p_value_greater)

    #distrubtion of the rwr scores
    plt.hist(background_scores_rwr, edgecolor='black', bins=50)   
    plt.axvline(average_stationary_feq, color='red')
    plt.xlabel("Average RWR")
    plt.ylabel("Frequency")  
    plt.show()        

    #predict novel tumorigenic genes

    #make the seed indices for the restart matrix with all 7 tumorigenic gene
    seed_indices = [node_index[g] for g in tumorgenic_genes if g in node_index]
    #rwr for predicted novel tumorigenic genes
    stationary_vector = rwr_predict(transition_matrix, seed_indices, 0.4, 1e-6, 100000)
    #make dictionary with all of the scores of the genes without the tumorgenic genes in it
    all_scores = {node: stationary_vector[i] for node, i in node_index.items() if node not in tumorgenic_genes}
    #sort them by highest to lowest score
    top_30_candidates = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:30]
    #putting the top 30 into the list without the scores
    top_30_genes = [gene for gene, score in top_30_candidates]
    #put the top 30 genes into the file
    with open("Kaitlyn_Carrillo_onco_predictions_1.txt", "w") as f:
        for u in top_30_genes:
            f.write(f"{u}\n")

    #randomized graph with swapped edges
            
    randomized_graph = networkx_graph.copy()
    nx.double_edge_swap(randomized_graph, nswap=3*randomized_graph.number_of_edges(), max_tries=100000)        

    #makes an adjaceny matrix from the random graph
    nodes_random = list(randomized_graph.nodes())
    node_index = {node: i for i, node in enumerate(nodes_random)}
    length_nodes = len(nodes_random)
    adjacency_matrix_random = nx.adjacency_matrix(randomized_graph, nodes_random)

    #create the random transition matrix from the random adjacency matrix to put into the rwr function
    sum_columns_random = adjacency_matrix_random.sum(axis = 0)
    sum_columns_random[sum_columns_random == 0] = 1
    transition_matrix_random = (adjacency_matrix_random / sum_columns_random).toarray()

    random_average_stationary_feq, random_average_steps, cost_random = average_rwr(transition_matrix_random, tumorgenic_genes, 0.3, 1e-6, 100000)
    print(random_average_stationary_feq)
    print(random_average_steps)
    print(cost_random)
    
    background_random_scores = []
    for _ in range(1000):
        random_gene_sequences_rwr_random = random.sample(genes_without_tumor, 7)
        score, _, _ = average_rwr(transition_matrix_random, random_gene_sequences_rwr_random, 0.3, 1e-6, 100000)
        background_random_scores.append(score)

    p_value_rand = np.sum(np.array(background_random_scores) <= random_average_stationary_feq) / 1000
    print("Randomized graph p-value(lesser):", p_value_rand) 
    p_value_rand = np.sum(np.array(background_random_scores) >= random_average_stationary_feq) / 1000
    print("Randomized graph p-value(greater):", p_value_rand)    

    plt.hist(background_random_scores, edgecolor='black', bins=50)   
    plt.axvline(random_average_stationary_feq, color='red')
    plt.xlabel("Average RWR")
    plt.ylabel("Frequency")  
    plt.show()

