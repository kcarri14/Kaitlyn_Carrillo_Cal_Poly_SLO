import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import random

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
    for _ in range(max_iteration):
        new_tracker_matrix = (1 - gamma) * np.dot(tran_matrix, tracker_matrix) + gamma * restart_matrix
        #checks for convergence
        if np.linalg.norm(new_tracker_matrix - tracker_matrix, 1) < probability_limit:
            break
        #update tracker
        tracker_matrix = new_tracker_matrix
    return tracker_matrix    

def spearman(node_rank_list, rwr_scores):
    correlation, p_val = spearmanr(node_rank_list, rwr_scores)
    return correlation, p_val

def average_rwr(transition_matrix, gamma, convergence, max_iteration):
    tumor_scores = []
    with open("onco_genes.txt", "r") as file:
        tumorgenic_genes = [gene.strip() for gene in file]
    for genes in tumorgenic_genes:
        seed_index = node_index[genes]
        stationary = rwr(transition_matrix, seed_index, gamma, convergence, max_iteration) 

        scores = [
        stationary[node_index[g]]
        for g in tumorgenic_genes
        if g != genes and g in node_index
        ]
    
        if scores:
            tumor_scores.append(np.mean(scores))

    average_rwr_score = np.mean(tumor_scores)

    return average_rwr_score
        


if __name__ == "__main__":
    #make graph from picture
    # toy_graph = nx.Graph()
    # #add the edges to the graph
    # edges = [("A", "B"),("A", "C"),("A", "H"),("A", "J"),("A", "K"),("B", "C"),("B", "D"),
    #          ("C", "E"),("D", "F"),("E", "G"),("F", "G"),("H", "I"),("I", "J") ]
    # toy_graph.add_edges_from(edges)
    
    # toy_graph_with_weights = nx.Graph()

    # edges_with_weights = [("A", "B", 4.0),("A", "C", 4.0),("A", "H", 4.0),("A", "J", 4.0),("A", "K", 1.0),("B", "C", 1.0),("B", "D", 1.0),
    #          ("C", "E", 1.0),("D", "F", 1.0),("E", "G", 1.0),("F", "G", 1.0),("H", "I", 1.0),("I", "J", 1.0) ]

    # toy_graph_with_weights.add_weighted_edges_from(edges_with_weights)

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
    # start_node = "A"
    # start_index = node_index[start_node]
    # stationary_frequency = rwr(transition_matrix, start_index, 0, 1e-6, 100000)

    # #sums up the frequency to make sure that they are equal to 1
    # sum_frequency = np.sum(stationary_frequency)
    # print(sum_frequency)

    # #creates a dictionary of the node and their value
    # stationary_frequency_dict = {node: stationary_frequency[i] for node, i in node_index.items()}

    # #puts them into two files so i can put it into cytpscape to make graph
    # with open("ppi_network.edgelist_weights", "w") as f:
    #     f.write("source target\n")  # header
    #     for u, v in graph.edges():
    #         f.write(f"{u} {v}\n")

    # rwr_scores_file = pd.DataFrame({
    #     "gene": list(stationary_frequency_dict.keys()),
    #     "RWR_score": list(stationary_frequency_dict.values())
    # })
    # rwr_scores_file.to_csv("rwr_scores_weights_1.csv", index=False)

    # rwr_score = list(stationary_frequency_dict.values())
    # rank = [5, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1]

    # core, p = spearman(rank, rwr_score)
    # print(core)
    # print(p)

    average_stationary_feq = average_rwr(transition_matrix, 0.3, 1e-6, 100000)



