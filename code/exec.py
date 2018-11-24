#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import argparse
from optparse import OptionParser
import Heuristics
import BranchAndBound as bnb
import LS

# File for my executable
# For example: type "python exec.py -inst "../Data/jazz.graph" -alg "Approx" -time 600 -seed 8" in your terminal

def main():

    parser = argparse.ArgumentParser(description="arguments")
    parser.add_argument('-inst', help='path to input graph', required = True)
    parser.add_argument('-alg', help='algorithm choice[BnB|Approx|LS1|LS2]', required = True)
    parser.add_argument('-time', help='cutoff time in seconds', required = True)
    parser.add_argument('-seed', help='seed', required = True)

    args = parser.parse_args()
    input_graph = args.inst
    algs = args.alg
    cutoff_time = int(args.time)
    if args.seed != None:
        seed = int(args.seed)


    if algs == "BnB":
        bnb.run_bnb(input_graph, cutoff_time)
    else:
        if algs == "Approx":
            Heuristics.Heur(input_graph, cutoff_time,seed)
        else:
            if algs == "LS1":
                runexp = LS.LS(input_graph, cut_time= int(float(cutoff_time)), alg = 'LS1', randseed=float(seed))
                C_star = runexp.LS1()
                print('length final cover: ' + str(C_star))
            else:
                if algs == "LS2":
                    runexp = LS.LS(input_graph, cut_time=int(float(cutoff_time)), alg='LS2', randseed=float(seed))
                    C_star = runexp.LS2()
                    print('length final cover: ' + str(C_star))
                else:
                    print "error: please choose among [BnB|Approx|LS1|LS2]"
                    exit(1)

if __name__ == '__main__':
    main()


