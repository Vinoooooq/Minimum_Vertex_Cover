import networkx as nx
import utilForBnB as util
import operator
import time
import os
import sys
import copy

class Bnb:

	def __init__(self, cutOffTime, output_trace):
		self.lowerBound = sys.maxint
		self.vc = []
		self.cutOffTime = cutOffTime
		self.start = time.time()
		self.output_trace = output_trace

	def writeTrace(self, file, currTime, solSize):
		file.write("%.2f,%d\n" %(currTime, solSize))
		

	def max_degree_vertex(self, G, sub_V):
		"""return the max degree vertex among the vertices in sub_V in graph G"""
		if not set(sub_V) <= set(G.nodes()):
			raise KeyError("max_degree_vertex(): vertices are not all in the graph")
			return None
		vertex_degree_dict = nx.degree(G, sub_V)
		return max(vertex_degree_dict.iteritems(), key = operator.itemgetter(1))[0]

	def residual_graph(self, G, removal_V):
		"""return the residual graph after removing all the vertices in the removal_V
		list, and all the vertices whose neighbor are all in removal_V"""
		if not isinstance(removal_V, list):
			removal_V = [removal_V]
		return [ v for v in G.nodes() if (v not in removal_V and not set(G.neighbors(v)) < set(removal_V)) ]

	def getVertexCover(self, G, usedV, unusedV):
		usedTime = time.time() - self.start
		if (usedTime >= self.cutOffTime):
			# writeSol()
			print "runout time"
			return 

		if (len(usedV) >= self.lowerBound):
			# print "boundFirst"
			return

		if ((len(G.edges()) - len(G.edges(usedV))) == 0):
			self.vc = copy.deepcopy(usedV)
			self.lowerBound = len(self.vc)
			currTime = time.time() - self.start
			self.writeTrace(self.output_trace, currTime, len(self.vc))
			print "vertex cover found - size " + str(self.lowerBound)
			return

		currLB = len(usedV) + len(nx.maximal_matching(G.subgraph(unusedV)))
		if (currLB > self.lowerBound):
			# print "bound!" + str(time.time() - self.start)
			return



		subGraph = G.subgraph(unusedV)
		maxDegreeV = self.max_degree_vertex(subGraph, unusedV)
		neighbors_maxV = G.neighbors(maxDegreeV)
		# print maxDegreeV

		leftGraph = G.subgraph(G.nodes())
		rightGraph = G.subgraph(G.nodes())

		leftUsedV = copy.deepcopy(usedV)
		leftUnusedV = copy.deepcopy(unusedV)
		leftUsedV.append(maxDegreeV)
		leftUnusedV.remove(maxDegreeV)
		# print leftUsedV
		# print leftUnusedV
		rightUsedV = copy.deepcopy(usedV)
		rightUsedV.extend(neighbors_maxV)
		rightUsedV = list(set(rightUsedV))
		rightUnusedV = self.residual_graph(G, rightUsedV)
		# print rightUsedV
		# print rightUnusedV

		

		# rightParameter = len(util.getLowerBound(G.subgraph(rightUnusedV)))
		# leftParameter = len(util.getLowerBound(G.subgraph(leftUnusedV)))
		rightParameter = len(nx.maximal_matching(G.subgraph(rightUnusedV))) * 2
		leftParameter = len(nx.maximal_matching(G.subgraph(leftUnusedV))) * 2
		rightVal = len(rightUsedV) + rightParameter
		leftVal = len(leftUsedV) + leftParameter
		
		if ((rightVal <= self.lowerBound) and (leftVal <= self.lowerBound)) :
			if (leftVal < rightVal) :
				self.lowerBound = leftVal
				self.getVertexCover(G, leftUsedV, leftUnusedV)
				self.getVertexCover(G, rightUsedV, rightUnusedV)
				return
			else:
				# self.lowerBound = leftVal
				self.getVertexCover(G, rightUsedV, rightUnusedV)
				self.getVertexCover(G, leftUsedV, leftUnusedV)
				return
		elif (len(leftUsedV) + leftParameter / 2 <= self.lowerBound):
			self.getVertexCover(G, leftUsedV, leftUnusedV)
			return
		# elif (len(rightUsedV) + rightParameter / 2 <= self.lowerBound):
		# 	self.getVertexCover(G, rightUsedV, rightUnusedV)
		# 	print 'once'
		# 	return
		else:
			return

def run_bnb(input_file, cutoff_time):
	start = input_file.rfind("/")
	end = input_file.find(".graph")
	filename = input_file[start+1:end]

	output_sol = "./output/" + filename + "_BnB_" + str(cutoff_time) + ".sol"
	output_trace = "./output/" + filename + "_BnB_" + str(cutoff_time) + ".trace"

	


	try:
		os.makedirs("./output")
	except OSError:
		if not os.path.isdir("./output"):
			raise
	outputTrace = open(output_trace, 'w')
	
	G = util.readGraph(input_file)
	unusedV = G.nodes()
	
	bnbSolver = Bnb(cutoff_time, outputTrace)
	bnbSolver.getVertexCover(G, [], unusedV)
	outputSol = open(output_sol, 'w')
	outputSol.write("%d\n" %len(bnbSolver.vc))
	res = list(bnbSolver.vc)
	res = sorted(res)
	for i in range(len(res)):
		outputSol.write("%d,"%(res[i]))
	outputSol.close()

if __name__ == '__main__':
	filename = './Data/delaunay_n10.graph'
	run_bnb(filename, 600)


