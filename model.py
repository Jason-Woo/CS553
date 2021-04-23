import numpy as np
import copy
from datetime import datetime
from genetic_alg import *


class Model(object):
    def __init__(self):
        self.target = -1
        self.candidates = []
        self.adjacency_list = []

        self.checkin_time_list = []
        self.check_loc_list = []

        self.recomm_size = 10

    def input_data(self):
        edges_file = '../brightkite/Brightkite_edges.txt'
        checkin_file = '../brightkite/Brightkite_totalCheckins.txt'

        f1 = open(edges_file, "r")
        lines = f1.readlines()
        curr = -1
        for line in lines:
            node1, node2 = map(int, line.strip().split())
            if node1 != curr:
                curr = node1
                self.adjacency_list.append([])
            self.adjacency_list[curr].append(node2)

        f2 = open(checkin_file, "r")
        lines = f2.readlines()
        curr_usr = 0
        curr_time_list = []
        curr_loc_list = []
        for line in lines:
            line0 = line.strip().split()
            if len(line0) == 5:
                usr_id, time, _, _, loc_id = line.strip().split()
                if int(usr_id) == curr_usr:
                    curr_time_list.append(time)
                    curr_loc_list.append(loc_id)
                else:
                    self.checkin_time_list.append(copy.deepcopy(curr_time_list))
                    self.check_loc_list.append(copy.deepcopy(curr_loc_list))
                    curr_usr += 1
                    while int(usr_id) != curr_usr:
                        self.checkin_time_list.append([])
                        self.check_loc_list.append([])
                        curr_usr += 1
                    curr_time_list = [time]
                    curr_loc_list = [loc_id]
        self.checkin_time_list.append(copy.deepcopy(curr_time_list))
        self.check_loc_list.append(copy.deepcopy(curr_loc_list))

    def k_hops(self, k):
        visited = []
        curr = [self.target]
        for _ in range(k):
            if not curr:
                break
            curr_neighbor = []
            for node in curr:
                for tmp_node in self.adjacency_list[node]:
                    if tmp_node not in visited:
                        visited.append(tmp_node)
                        curr_neighbor.append(tmp_node)
            curr.clear()
            curr = curr_neighbor
        return visited

    def similar_time(self, time1, time2, threshold=300):
        # 2008-12-29T01:58:37Z
        t1 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%SZ")
        t2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")
        if abs(t1 - t2).second <= threshold:
            return True
        else:
            return False

    def similar_mobility(self):
        target_time = self.checkin_time_list[self.target]
        target_loc = self.check_loc_list[self.target]
        candidate = []
        for i, loc_list in enumerate(self.check_loc_list):
            find = False
            for j, loc in enumerate(loc_list):
                for k, tar_loc in enumerate(target_loc):
                    if tar_loc == loc and target_time[k] == self.checkin_time_list[i][j]:
                        candidate.append(i)
                        find = True
                        break
                if find:
                    break
        candidate.remove(self.target)
        return candidate

    def filtering(self):
        self.candidates = self.k_hops(2)
        for node in self.similar_mobility():
            if node not in self.candidates:
                self.candidates.append(node)

    def neighbor_ints(self, curr):
        # intersection
        neighbor_tar = self.adjacency_list[self.target]
        neighbor_curr = self.adjacency_list[curr]
        neighbor_comm = [i for i in neighbor_curr if i in neighbor_tar]
        return neighbor_comm

    def neighbor_union(self, curr):
        # union
        neighbor_tar = self.adjacency_list[self.target]
        neighbor_curr = self.adjacency_list[curr]
        for i in neighbor_curr:
            if i not in neighbor_tar:
                neighbor_tar.append(i)
        return neighbor_tar

    def adjacent_nodes(self, curr):
        neighbor_comm = self.neighbor_ints(curr)
        return len(neighbor_comm)

    def density_ints(self, curr):
        neighbor_comm = self.neighbor_ints(curr)
        edge_num, vertex_num = 0, len(neighbor_comm)
        for i in neighbor_comm:
            for j in self.adjacency_list[i]:
                if j in neighbor_comm:
                    edge_num += 1
        edge_num /= 2
        density = (2 * edge_num) / (vertex_num * (vertex_num - 1))
        return density

    def density_union(self, curr):
        neighbor = self.neighbor_union(curr)
        edge_num, vertex_num = 0, len(neighbor)
        for i in neighbor:
            for j in self.adjacency_list[i]:
                if j in neighbor:
                    edge_num += 1
        edge_num /= 2
        density = (2 * edge_num) / (vertex_num * (vertex_num - 1))
        return density

    def mobility_similarity(self, curr):
        # TODO
        return 1

    def get_idx(self):
        index = np.zeros((len(self.candidates), 4))
        for i, c in enumerate(self.candidates):
            index[i] = [self.adjacent_nodes(c), self.density_ints(c), self.density_union(c), self.mobility_similarity(c)]

        idx_min = index.min(axis=0)
        idx_max = index.max(axis=0)
        index_normed = (index - idx_min) / (idx_max - idx_min)
        return index_normed

    def run(self):
        index = self.get_idx()
        genetic = GeneticAlg(index, self.candidates, self.adjacency_list[self.target])
        weight = genetic.run()
        score = np.dot(weight.T, index)
        score_list = score.tolist()
        recomm_list = []
        while len(recomm_list) < self.recomm_size:
            best_idx = score_list.index(min(score_list))
            if self.candidates[best_idx] not in self.adjacency_list[self.target]:
                recomm_list.append(self.candidates[best_idx])
        return recomm_list

