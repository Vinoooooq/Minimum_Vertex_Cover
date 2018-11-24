#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import time
import random
import networkx as nx
from random import choice
import os
import argparse

# This function for read the file and change them into right data structure
def Readfile(filename):
    file=open(filename)
    file=file.read().splitlines()
    for i in range(len(file)):
        file[i]=file[i].split(' ')
    k=len(file)
    for i in range(1,k):
        file[i].pop()
    for i in range(len(file)):
        subfile=file[i]
        for j in range(len(subfile)):
            subfile[j]=int(subfile[j])
    file.pop()
    k=len(file)

    G=nx.Graph()
    for i in range(file[0][0]):
        G.add_node(i+1)
    for i in range(k):
        if i == 0:
            continue
        for j in range(len(file[i])):
            G.add_edge(i,file[i][j])

    V=G.nodes()
    E=G.edges()
    return (V,E,G)


# This function is to compute the MVC using Edge Deletion
def Heuristics(VV,EE,GG):
    V=VV
    E=EE
    G=GG.copy()
    V_MVC=[]
    while E != []:
        Vino=choice(E)
        V_MVC.append(Vino[0])
        V_MVC.append(Vino[1])
        G.remove_nodes_from([Vino[0],Vino[1]])
        V=G.nodes()
        G=G.subgraph(V)
        E=G.edges()

    return V_MVC

# main function, running the algorithm for 10 mins and record the outputs we want
def Heur(input_graph,cutoff_time,seed):
    try:
        os.makedirs("./output")
    except OSError:
        if not os.path.isdir("./output"):
            raise
    start = input_graph.rfind("/")
    end = input_graph.find(".graph")
    filename = input_graph[start+1:end]
    random.seed(seed)
    (VV,EE,GG)=Readfile(input_graph)
    start_time=time.time()
    Vino=10**5
    Vino_nodes=[]
    while time.time()-start_time <= cutoff_time:
        V_MVC=Heuristics(VV,EE,GG)
        if len(V_MVC) < Vino:
            Vino=len(V_MVC)
            Vino_nodes=V_MVC
            Vino_nodes=sorted(Vino_nodes)
            elapsed_time=time.time()-start_time
            output_trace=open("./output/" + filename + "_Heur_" + str(cutoff_time) + "_" +str(seed)+ ".trace",'a')
            output_trace.write(str(elapsed_time) + ',' + str(Vino) + '\n')
            print "new vertex cover got! Length:" + str(Vino)
    print "final vertex cover length:" + str(Vino)
    # print "final vertex cover:" + str(Vino_nodes)
    print "time elapsed:" + str(time.time()-start_time)

    # print(os.path.relpath('/Users/guowanyang/Downloads/Data/karate.graph'))
    # "./output/" + filename + "_BnB_" + str(cutoff_time) + ".sol"

    output=open("./output/" + filename + "_Heur_" + str(cutoff_time) + "_" +str(seed)+ ".sol",'w')
    output.write(str(Vino) +'\n' + str(Vino_nodes))


if __name__ == "__main__":
    # Heur('../../../Downloads/Data/star2.graph',600)
    Heur()




