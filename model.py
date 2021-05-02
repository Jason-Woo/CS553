import numpy as np
import copy
from datetime import datetime
from genetic_alg import *
from DAO import *


class Model(object):
    def __init__(self, tar, baseline=True):
        self.target = tar
        self.candidates = []
        self.adjacency_list = []

        self.recomm_size = 100
        self.baseline = baseline

    def input_data(self, adjacency_list):
        self.adjacency_list = adjacency_list

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

    # def similar_time(self, time1, time2, threshold=300):
    #     # 2008-12-29T01:58:37Z
    #     t1 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%SZ")
    #     t2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")
    #     if abs(t1 - t2).seconds <= threshold:
    #         return True
    #     else:
    #         return False

    # def similar_mobility(self):
    #     target_time = self.checkin_time_list[self.target]
    #     target_loc = self.check_loc_list[self.target]
    #     candidate = []
    #     for i, loc_list in enumerate(self.check_loc_list):
    #         find = False
    #         for j, loc in enumerate(loc_list):
    #             for k, tar_loc in enumerate(target_loc):
    #                 if tar_loc == loc and target_time[k] == self.checkin_time_list[i][j]:
    #                     candidate.append(i)
    #                     find = True
    #                     break
    #             if find:
    #                 break
    #     candidate.remove(self.target)
    #     print(candidate)
    #     return candidate

    def similar_mobility(self):
        candidate = []
        self.mobility_tups_5_min = {}
        self.mobility_tups_60_min = {}
        result_5_min = query_database(build_sql(self.target, 5))
        result_60_min = query_database(build_sql(self.target, 60))
        for i in result_5_min:
            self.mobility_tups_5_min[i[0]] = i[1]
        for i in result_60_min:
            candidate.append(i[0])
            self.mobility_tups_60_min[i[0]] = i[1]
        return candidate

    def filtering(self, k=2):
        print("Start Filtering")
        self.candidates = self.k_hops(k)
        for node in self.similar_mobility():
            if node not in self.candidates:
                self.candidates.append(node)
        self.candidates.remove(self.target)
        print("Filtering Done, #candidates=", len(self.candidates))

    def neighbor_ints(self, curr):
        # intersection
        neighbor_tar = self.adjacency_list[self.target]
        neighbor_curr = self.adjacency_list[curr]
        neighbor_comm = [i for i in neighbor_curr if i in neighbor_tar]
        return neighbor_comm

    def neighbor_union(self, curr):
        # union
        neighbor_tar = copy.deepcopy(self.adjacency_list[self.target])
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
        if vertex_num == 0 or vertex_num == 1:
            return 0
        else:
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
        if vertex_num == 0 or vertex_num == 1:
            return 0
        else:
            density = (2 * edge_num) / (vertex_num * (vertex_num - 1))
        return density

    # def mobility_similarity(self, curr):
    #     target_loc = self.check_loc_list[self.target]
    #     target_time = self.checkin_time_list[self.target]
    #     curr_loc = self.check_loc_list[curr]
    #     curr_time = self.checkin_time_list[curr]
    #     similarity = 0
    #     for i, loc1 in enumerate(target_loc):
    #         for j, loc2 in enumerate(curr_loc):
    #             if loc1 == loc2 and self.similar_time(target_time[i], curr_time[j]):
    #                 similarity += 1
    #     return similarity

    def mobility_similarity_5_min(self, curr):
        if curr not in self.mobility_tups_5_min:
            return 0
        return self.mobility_tups_5_min[curr]

    def mobility_similarity_60_min(self, curr):
        if curr not in self.mobility_tups_60_min:
            return 0
        return self.mobility_tups_60_min[curr]

    def get_idx(self):
        index = np.zeros((len(self.candidates), 4))
        for i, c in enumerate(self.candidates):
            if i % 100 == 0:
                print("\rIndexing: {a}/{b}".format(a=i, b=len(self.candidates)), end="")
            index[i] = [self.adjacent_nodes(c), self.density_ints(c), self.density_union(c),
                        self.mobility_similarity_5_min(c)]
        # idx_min = index.min(axis=0)
        # idx_max = index.max(axis=0)
        # index_normed = (index - idx_min) / (idx_max - idx_min)
        print('\n', end='')
        print("Indexing done")
        # return index_normed
        return index

    def run(self):
        index = self.get_idx()
        print("--------------------------Genetic Algorithm--------------------------")
        genetic = GeneticAlg(index, self.candidates, self.adjacency_list[self.target])
        weight = genetic.run()
        score = np.dot(index, weight)
        score_list = score.tolist()
        recomm_list = []
        while len(recomm_list) < self.recomm_size:
            # best_idx = score_list.index(max(score_list))
            best_idx = score_list.index(min(score_list))
            if self.candidates[best_idx] not in self.adjacency_list[self.target]:
                recomm_list.append(self.candidates[best_idx])
            score_list[best_idx] = 99999999
            # score_list[best_idx] = -1
        if self.baseline:
            print('--------------------------Genetic Algorithm (Baseline)--------------------------')
            index_baseline = index[:, :-1]
            genetic_baseline = GeneticAlg(index_baseline, self.candidates, self.adjacency_list[self.target])
            weight_baseline = genetic_baseline.run()
            score_baseline = np.dot(index_baseline, weight_baseline)
            score_list_baseline = score_baseline.tolist()
            recomm_list_baseline = []
            while len(recomm_list_baseline) < self.recomm_size:
                best_idx_baseline = score_list_baseline.index(min(score_list_baseline))
                if self.candidates[best_idx_baseline] not in self.adjacency_list[self.target]:
                    recomm_list_baseline.append(self.candidates[best_idx_baseline])
                score_list_baseline[best_idx_baseline] = 99999999
            return recomm_list, recomm_list_baseline
        else:
            return recomm_list, []

        # np.savetxt("tmp.csv", index, delimiter=",")
        # np.savetxt("tmp1.csv", self.candidates, delimiter=",")
        # np.savetxt("tmp2.csv", self.adjacency_list[self.target], delimiter=",")
