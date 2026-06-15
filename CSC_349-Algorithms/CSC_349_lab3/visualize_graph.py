import sys
import math
import collections
import networkx as nx
import matplotlib.pyplot as plt
from node import node, read_file


def visualize_graph(nodes, weighted=False, directed=True, layout="spring"):
    """
    Visualizes a graph using NetworkX.

    Parameters:
    - nodes: Dictionary of Node objects
    - weighted: If True, assumes edges are tuples (node, weight)
    - directed: If True, uses a directed graph representation
    - layout: One of "spring", "kamada_kawai", "planar", or "shell"
    """
    G = nx.DiGraph() if directed else nx.Graph()

    # Add nodes
    for node in nodes.values():
        G.add_node(node.name)

    # Add edges
    for node in nodes.values():
        edge_list = node.out_edges
        for edge in edge_list:
            if weighted:
                neighbor, weight = edge  # Tuple (Node, Weight)
                G.add_edge(node.name, neighbor.name, weight=weight)
            else:
                G.add_edge(node.name, edge.name)

    seed = 42

    # Use a dictionary to dynamically handle different layout types
    layout_functions = {
        "spring": lambda G: nx.spring_layout(G, seed=seed),
        "kamada_kawai": lambda G: nx.kamada_kawai_layout(G),  # No seed
        "spectral": lambda G: nx.spectral_layout(G),  # No seed
        "random": lambda G: nx.random_layout(G, seed=seed),
        "circular": lambda G: nx.circular_layout(G),
        "shell": lambda G: nx.shell_layout(G),
    }

    # Get the layout function, default to spring_layout if unknown
    pos = layout_functions.get(layout, layout_functions["spring"])(G)

    # Draw graph
    plt.figure(figsize=(7, 5))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray", arrowsize=20)

    # Draw weights if weighted
    if weighted:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=12)

    plt.show()


def main():
    """
    Parses command-line arguments and runs the graph visualization.
    
    Usage:
    python script.py <filename>  [--weighted] [--directed]
    
    - <filename>: Path to the input file containing graph data.
    - --weighted: If provided, the graph edges will be treated as weighted.
    - --directed: If provided, the graph will be considered directed.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>  [--weighted] [--directed]")
        sys.exit(1)
    
    filename = sys.argv[1]
    allowed_algorithms = ["PRIM", "KRUSKAL"]
    
    
    weighted = "--weighted" in sys.argv  # Check if --weighted is passed
    directed = "--directed" in sys.argv  # Default to undirected unless --directed is provided
    
    G, E = read_file(filename, weighted=weighted, directed=directed)
    visualize_graph(G, weighted=weighted, directed=directed, layout="planar ")


if __name__ == '__main__':
    main()
