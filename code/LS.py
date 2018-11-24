import time
import networkx as nx
import random
import copy
import numpy as np

class LS:

    def __init__(self, filename, cut_time = 60, randseed = 5, alg = 'LS1'):
        self.filename = filename
        self.cut_time = cut_time
        self.randseed = randseed
        name = filename.replace('.graph', '')
        self.sol_file = name + '_' + alg + '_' + str(cut_time) + '_' + str(int(randseed)) + '.sol'
        self.trace_file = name + '_' + alg + '_' + str(cut_time) + '_' + str(int(randseed)) + '.trace'
        self.report_file = name + '_' + alg + '_' + str(cut_time) + '_' + str(int(randseed)) + '.rep'
        self.G = None

    def read_graph(self):
        file = open(self.filename, 'r')
        edge_list = file.readlines()
        del edge_list[0]
        i = 1
        for line in edge_list:#
            edge_list[i - 1] = str(i) + ' ' + line
            i += 1
        self.G = nx.parse_adjlist(edge_list, create_using=nx.Graph(), nodetype=int)
        print("done")

    def is_cover(self, C):
        for e in self.G.edges():
            if e[0] not in C and e[1] not in C:
                return False
        return True

    def cost(self, C, v):
        cost = 0
        missing = []
        for e in self.G.edges():
            if (e[0] not in C or e[0] == v) and (e[1] not in C or e[1] == v):
                cost += 1
                if e[0] not in C or e[0] == v:
                    missing.append(e[0])
                else:
                    missing.append(e[1])

        return cost, missing

    def gain(self, C, cost_c, v):
        cost = 0
        missing = []
        for e in self.G.edges():
            if (e[0] not in C and e[0] != v) and (e[1] not in C and e[1] != v):
                cost += 1
                if e[0] not in C or e[0] == v:
                    missing.append(e[0])
                else:
                    missing.append(e[1])

        return cost - cost_c

    def min_cost_k(self, C, k):
        min_cost = float('Inf')
        for j in range(0, k):
            i = random.randint(0, len(C)-1)
            v = C[i]
            cost, v_missing = self.cost(C, v)
            if cost < min_cost:
                best_v = v
                min_cost = cost
        return best_v, min_cost

    def max_gain_k(self, C, cost_c, I, k):
        max_gain = - float('Inf')
        i = random.randint(0, len(I)-1)
        for j in range(0, k):
            v = I[i]
            gain = self.gain(C, cost_c, v)
            if gain > max_gain:
                best_v = v
                best_cost = cost_c + gain
        return best_v, best_cost

    def construct_vc(self):
        C = []
        I = []
        #C = self.G._node.keys()
        for e in self.G.edges():
            if e[0] not in C and e[1] not in C:
                if self.G.degree(e[0]) > self.G.degree(e[1]):
                    C.append(e[0])
                else:
                    C.append(e[1])

        for node in self.G.nodes():
            if node not in C:
                I.append(node)

        return copy.deepcopy(C), copy.deepcopy(I)

    def degree(self, v):
        return self.G.degree(v)/nx.number_of_edges(self.G)

    def LS1(self):
        random.seed(self.randseed)
        self.read_graph()
        k = 50
        C, I = self.construct_vc()

        print("length initial cover: " + str(len(C)))
        C_star = []

        f_trace = open(self.trace_file, 'w')
        f_sol = open(self.sol_file, 'w')
        f_rep = open(self.report_file, 'a')

        start = time.clock()
        end = start + self.cut_time

        print("start time: " + str(start))
        print("cut off: " + str(end))
        while time.clock() < end:
            while self.is_cover(C) and time.clock() < end:

                # save best solution C*
                C_star = copy.deepcopy(C)
                f_trace.write(str(time.clock()) + ', ' + str(len(C_star)) + '\n')

                # ind_remove = index of node with minimum loss after removal,
                # v_missing = nodes to edge missing (not in C)
                v_remove, cost_c = self.min_cost_k(C, k)

                # remove node
                I.append(v_remove)
                del C[C.index(v_remove)]

            # ind_remove = index of node with minimum loss after removal,
            # v_missing = nodes tc edge missing (not in C)
            v_remove, cost_c = self.min_cost_k(C, k)

            # remove node
            I.append(v_remove)
            del C[C.index(v_remove)]

            # find missing node with best gain
            v_add, cost_c = self.max_gain_k(C, cost_c, I, k)
            C.append(v_add)
            del I[I.index(v_add)]

        final_end = time.clock()
        run_time = final_end - start
        f_sol.write(str(len(C_star)) + '\n')
        f_sol.write(','.join(map(str, C_star)))
        f_rep.write(str(run_time) + ',' + str(len(C_star)) + ' \n')
        print("final time: " + str(final_end))
        #true_cover = min_weighted_vertex_cover(self.G)
        return len(C_star)

    def LS2(self):
        random.seed(self.randseed)
        self.read_graph()
        k = 3
        C, I = self.construct_vc()
        cost_c_last, m = self.cost(C, None)
        obj_last = len(C) + cost_c_last
        cost_star = cost_c_last
        print("length initial cover: " + str(len(C)))
        C_star = copy.deepcopy(C)
        f_trace = open(self.trace_file, 'w')
        f_sol = open(self.sol_file, 'w')
        f_rep = open(self.report_file, 'a')

        f_trace.write(str(time.clock()) + ', ' + str(len(C_star)) + '\n')
        start = time.clock()
        end = start + self.cut_time


        print("start time: " + str(start))
        print("cut off: " + str(end))
        while time.clock() < end:


            # if solution is better than before
            if self.is_cover(C) and len(C) < len(C_star):
                # save best solution C*
                C_star = copy.deepcopy(C)
                f_trace.write(str(time.clock()) + ', ' + str(len(C_star)) + '\n')

            # pick random node to remove
            v_remove, cost_c = self.min_cost_k(C, 1)
            obj = cost_c + len(C) - 1
            if obj < obj_last:
                I.append(v_remove)
                del C[C.index(v_remove)]
                obj_last = obj
                cost_c_last = cost_c

            #if solution is worse compute probability
            else:
                rem_time = (end - time.clock())/end
                obj_diff = obj - obj_last
                p1 = np.exp(-obj_diff*(1 - self.degree(v_remove))/rem_time)/100
                if random.random() < p1:
                    I.append(v_remove)
                    del C[C.index(v_remove)]
                    cost_c_last = cost_c
                    obj_last = obj

            if self.is_cover(C) and len(C) < len(C_star):
                # save best solution C*
                C_star = copy.deepcopy(C)
                f_trace.write(str(time.clock()) + ', ' + str(len(C_star)) + '\n')

            # pick random node to add
            v_add, cost_c = self.max_gain_k(C, cost_c_last, I, 1)
            obj = cost_c + len(C) + 1
            if obj < obj_last:
                C.append(v_add)
                del I[I.index(v_add)]
                cost_c_last = cost_c
                obj_last = obj

            # if solution is worse compute probability
            else:
                rem_time = (end - time.clock()) / end
                obj_diff = obj - obj_last
                p2 = np.exp(-obj_diff*(1 + self.degree(v_add)) / rem_time)/100
                if random.random() < p2:
                    C.append(v_add)
                    del I[I.index(v_add)]
                    cost_c_last = cost_c
                    obj_last = obj

        final_end = time.clock()
        run_time = final_end - start
        f_sol.write(str(len(C_star))+ '\n')
        f_sol.write(','.join(map(str, C_star)))
        f_rep.write(str(run_time) + ',' + str(len(C_star)) + ' \n')
        print("final time: " + str(final_end))
        return len(C_star)