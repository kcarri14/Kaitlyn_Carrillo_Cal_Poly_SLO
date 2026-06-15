import sys
import math
import collections
import networkx as nx
import matplotlib.pyplot as plt

class node:
    def __init__(self, name, out_edges, in_edges, previsit, postvisit, component):
        self.name = name
        self.out_edges = out_edges
        self.in_edges = in_edges
        self.previsit = previsit
        self.postvisit = postvisit
        self.component = component
        self.key = float('inf')
        self.parent = None
        self.in_MST = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name       

    def __lt__(self,other):
        return self.key < other.key




def read_file(filename, weighted=False, directed=True):
    with open(filename) as f:
        lines = f.readlines()
        v = int(lines[0].strip())
        if v == 0:
            raise ValueError("Graph must have one or more vertices")
        
        # Read vertex names
        G = {}
        E = []
        for i in range(1, v + 1):
            name = lines[i].strip()
            G[name] = node(name=name, out_edges=[], in_edges=[], previsit=-1, postvisit=-1, component=None)
        
        # Read edges
        for l in lines[v + 1:]:
            tokens = l.split(",")
            fromVertex, toVertex = tokens[0].strip(), tokens[1].strip()
            weight = int(tokens[2]) if weighted and len(tokens) > 2 else 1

            
            if weighted:
                E.append([(fromVertex,toVertex),weight])
                if directed:
                    G[fromVertex].out_edges.append((G[toVertex], weight))
                    G[toVertex].in_edges.append((G[fromVertex], weight))
                else:
                    G[fromVertex].out_edges.append((G[toVertex], weight))
                    G[toVertex].out_edges.append((G[fromVertex], weight))
                    
            else:
                E.append((fromVertex,toVertex))
                if directed:
                    G[fromVertex].out_edges.append(G[toVertex])
                    G[toVertex].in_edges.append(G[fromVertex])
                else:
                    G[fromVertex].out_edges.append(G[toVertex])
                    G[toVertex].out_edges.append(G[fromVertex])
        
        return G, E


def main():
    """
    Parses command-line arguments and runs the graph visualization.
    
    Usage:
    python script.py <filename> [--weighted] [--directed]
    
    - <filename>: Path to the input file containing graph data..
    - --weighted: If provided, the graph edges will be treated as weighted.
    - --directed: If provided, the graph will be considered directed.
    """
    if len(sys.argv) < 2:
        print("Usage: python node.py <filename> > --weighted] [--directed]")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    weighted = "--weighted" in sys.argv  # Check if --weighted is passed
    directed = "--directed" in sys.argv  # Default to undirected unless --directed is provided
    
    G, E = read_file(filename, weighted=weighted, directed=directed)
    # visualize_graph(G, weighted=weighted, directed=directed, layout="planar ")
    print(f"Read file {filename}")
    print(f"Vertices {G}")
    print(f"Edges{E}")

if __name__ == '__main__':
    main()
