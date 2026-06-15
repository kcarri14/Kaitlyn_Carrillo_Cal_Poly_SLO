import sys
import collections
import math

class node:
#code from source code
	def __init__(self,name,out_edges,in_edges,previsit,postvisit,component):
		self.name = name
		self.out_edges = out_edges
		self.in_edges = in_edges
		self.previsit = previsit
		self.postvisit = postvisit		
		self.component = component

#performs dfs to iterate through out-going edges
def dfs_round1(node, G, visited, stack):
    visited.add(node.name)
    for neighbor in node.out_edges:
        if neighbor not in visited:
            dfs_round1(G[neighbor], G, visited, stack)
    stack.append(node.name)

#performs dfs to iterate through in-going edges
def dfs_round2(node, G, visited, component):
	visited.add(node.name)
	component.append(node.name)
	for neighbor in node.in_edges:
		if neighbor not in visited:
			dfs_round2(G[neighbor],G, visited, component)

#returns connected components as a list of lists 
def strong_connectivity(G):
	visited =set()
	stack = collections.deque()
	strongly_connected = []
    
	for node in G:
		if node.name not in visited:
			dfs_round1(node,G,visited,stack)
			
	visited.clear()
	
	while stack:
		node_name = stack.pop()
		if node_name not in visited:
			component = []
			dfs_round2(G[node_name], G, visited, component)
			strongly_connected.append(component)
			
	sort_component_list(strongly_connected)		
	return strongly_connected

#sorts the strognly_connected list
def sort_component_list(components):
	for c in components:
		c.sort()
	components.sort(key = lambda x: x[0])
#reads file given
def read_file(filename):
	with open(filename) as f:
		lines = f.readlines()
		v = int(lines[0])
		if  v == 0:
			raise ValueError("Graph must have one or more vertices")
		G = list(node(name = i, in_edges=[],out_edges=[],previsit= -1, postvisit=-1, component=None) for i in range(v))
		for l in lines[1:]:
			tokens = l.strip().split(",")
			fromVertex,toVertex = (int(tokens[0]),int(tokens[1]))
			G[fromVertex].out_edges.append(toVertex)
			G[toVertex].in_edges.append(fromVertex)
		return G

def main():
	filename = sys.argv[1]
	G = read_file(filename)
	components = strong_connectivity(G)
	print(components)
		
		
if __name__ == '__main__':
	main()
