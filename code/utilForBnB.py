"""
This file provides some tools for BnB algorithm
1.Read data from source file and parse as networkx format graph
2.Get the lower bound for sub graph using matching
"""
import networkx as nx
import os
import os.path

def readGraph(filename):
	with open(filename) as graphData:
		graphInfo = graphData.readline()

		G = nx.Graph()
		nodeIdx = 1
		for line in graphData:
			neighbors = list(map(lambda x: int(x), line.split()))
			edges = [(nodeIdx, x) for x in neighbors]
			G.add_edges_from(edges)
			nodeIdx += 1
	return G

def getLowerBound(G):
	coverV = set()
	coverE = set()

	for u, v in G.edges_iter():
		if (u, v) not in coverE and (v, u) not in coverE:
			coverV.add(u)
			coverV.add(v)
			coverE = coverE | set(G.edges([u, v]))

	return list(coverV)

if __name__ == '__main__':
	filename = './Data/email.graph'
	G = readGraph(filename)
	print len(getLowerBound(G))