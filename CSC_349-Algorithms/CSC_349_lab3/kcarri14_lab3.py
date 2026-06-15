import sys 
from node import node, read_file



def MST_Prim(G, root):
    """
    Outputs a list of edges corresponding to an MST as calculated by Prim's algorithm
    To ensure consistent order, you're already given the root as the vertex with the lowest vertex name in lexicographic order
"""
    # do NOT change the  lines below
    total_weight = 0
    root.key = 0
    root.parent = root
    import heapq
    heap = []
    T = []
    heapq.heappush(heap,root)

 # while heap is not empty, pop v from heap and check if it is already in the MST (using v.in_MST)
    while heap:
       
        v = heapq.heappop(heap)
        if v.in_MST:
            continue
    # Then, if it is not, add it to the MST, append it to T and add its v.key to total weights
        v.in_MST = True
        # You can identify the root since for it, v.parent = v
        if v.parent != v:
            # For formatting consistency of the, append the edge to the root as a tuple (v,v.parent)
            T.append((v.name, v.parent.name))
            total_weight += v.key
    # Finally, iterate over negighbors u        
        for neighbor, weight in v.out_edges:
            #  for those whose edge cost is smaller than current key:
            if not neighbor.in_MST and weight < neighbor.key:
                 # update their key to the edge weight
                neighbor.key = weight
                # update their parent to v
                neighbor.parent = v
                # add them to the heap
                heapq.heappush(heap, neighbor)       
    return T, total_weight

def MST_Kruskal(G,E):
    # do NOT change the  lines below

    total_weight = 0
    T = []

    # Example of disjoint set manipulation: we start with each node as its own set

    from scipy.cluster.hierarchy import DisjointSet
    dijoint_set = DisjointSet(G)
    # Important operations in a disjoint set (see example of usage of each below)
    # print("Demonstration of Disjoint Set functionality")  
    # print("Before merging")
    # print(f"Subsets : {dijoint_set.subsets()}") # list subsets
    # print(f" Are a and b connected? {dijoint_set.connected('a','b')}") # check if two items are connected
    # print(f" The subset defined by a has {dijoint_set.subset('a')} as element, and {dijoint_set.__getitem__('a')} as representative") # check all elements in the set containing a givenitem, as well as its representative element
    # print(f" The subset defined by b has {dijoint_set.subset('b')} as element, and {dijoint_set.__getitem__('b')} as representative")
    # print("")
    # dijoint_set.merge('a','b') # We can merge the subsets given by two items. See results of the same operations after merging
    # print(f"Subsets : {dijoint_set.subsets()}")
    # print(f" Are a and b connected? {dijoint_set.connected('a','b')}")
    # print(f" The subset defined by a has {dijoint_set.subset('a')} as element, and {dijoint_set.__getitem__('a')} as representative")
    # print(f" The subset defined by b has {dijoint_set.subset('b')} as element, and {dijoint_set.__getitem__('b')} as representative")
    # print("")

 # Sort the edges by weight, then iterate over them in order
    E.sort(key=lambda x: x[1])

 # For each edge, check if its two endpoints are already connected
    
    for (u, v), weight  in E:
        # If they are NOT connected, connect them, add them to the tree and their weight to the total
        if not dijoint_set.connected(u,v):
            dijoint_set.merge(u,v)
            T.append((u,v))
            total_weight += weight
        # Otherwise, ignore the edge
        if len(T) == len(G) - 1:
            break
    return T, total_weight



def main():
    """
    Do NOT change main function
    Parses command-line arguments and runs the graph visualization.
    
    Usage:
    python script.py <filename> <algorithm>
    
    - <filename>: Path to the input file containing graph data.
    - <algorithm>: One of "PRIM", "KRUSKAL".

    """
    if len(sys.argv) < 3:
        print("Usage: python script.py <filename> <algorithm>")
        sys.exit(1)
    
    filename = sys.argv[1]
    algorithm = sys.argv[2].upper()
    allowed_algorithms = ["PRIM", "KRUSKAL"]
    
    if algorithm not in allowed_algorithms:
        print(f"Error: Invalid algorithm. Choose from {allowed_algorithms}")
        sys.exit(1)
    
    weighted = True  # Since we are building MST algorithms, we only care about weighted graphs
    directed = False # Let's ignore directed graphs for this assignment
    
    G, E = read_file(filename, weighted=weighted, directed=directed)
    # visualize_graph(G, weighted=weighted, directed=directed, layout="planar ")

    if algorithm == "PRIM":
        root = G[min(G.keys())]  # Do NOT change this line - the root should be the lowest node in lexicographical order for consistency
        MST, w = MST_Prim(G,root)
    if algorithm == "KRUSKAL":
        MST, w= MST_Kruskal(G,E)

    print(MST)
    print(w)


if __name__ == '__main__':
    main()
