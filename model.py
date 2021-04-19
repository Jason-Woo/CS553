import numpy as np


class Model(object):
    def __init__(self):
        self.target = -1
        self.candidates = []
        self.adjacency_list = []
        self.checkin_usr_list = []
        self.checkin_time_list = []
        self.check_loc_list = []

        self.population_size = 1000
        self.mutation_rate = 0.01
        self.max_iter = 1000

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
        for line in lines:
            line0 = line.strip().split()
            if len(line0) == 5:
                usr_id, time, _, _, loc_id = line.strip().split()
                self.checkin_usr_list.append(usr_id)
                self.checkin_time_list.append(time)
                self.check_loc_list.append(loc_id)

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

    def similar_time(self, time1, time2, threshold):
        # 2008-12-29T01:58:37Z
        #TODO
        return

    def similar_mobility(self):
        target_time = self.checkin_time_list[self.target]
        candidate = []
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
        # intersection
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

    def scoring(self, weight, index):
        avg_rank = []
        for i in range(self.population_size):
            tmp_rank = 0
            curr_weight = weight[i]
            score = np.dot(curr_weight.T, index)
            score_sorted_idx = np.argsort(-score)
            for j, c in enumerate(self.candidates):
                if c in self.adjacency_list[self.target]:
                    tmp_rank += score_sorted_idx[j]
            tmp_rank /= len(self.adjacency_list[self.target])
            avg_rank.append(tmp_rank)
        return avg_rank

    def keep_fittest(self, rank, population):
        rank_cpy = rank[:]
        population_fittest = []
        for _ in range(self.population_size):
            curr_min = rank_cpy.index(min(rank_cpy))
            population_fittest.append(population[curr_min])
            rank_cpy[curr_min] = 999
        return population_fittest

    def next_genration_helper(self, num1, num2):
        num1_bin = '{:08b}'.format(num1)
        num2_bin = '{:08b}'.format(num2)
        pos = np.random.randint(1, 8)
        new_bin = num1_bin[:pos] + num2_bin[pos:]
        for i in range(8):
            if np.random.rand() < self.mutation_rate:
                new_bin = new_bin[:i] + str(1 - int(new_bin[i])) + new_bin[i+1:]
        return int(new_bin, 2)

    def next_genration(self, population):
        new_population = []
        for i in range(self.population_size):
            for j in range(i + 1, self.population_size):
                parent1 = population[i]
                parent2 = population[j]
                child = []
                for k in range(4):
                    child.append(self.next_genration_helper(parent1[k], parent2[k]))
                new_population.append(child)
        return np.concatenate((population, new_population))

    def genetic_alg(self):
        population = np.random.randint(0, 256, (self.population_size, 4))
        idx = self.get_idx()
        rank = self.scoring(population, idx)

        best_rank = min(rank)
        cnt = 0
        best_rank_history = best_rank

        for _ in range(self.max_iter):
            population = self.next_genration(population)
            population = self.keep_fittest(rank, population)
            rank = self.scoring(population, idx)
            best_rank = min(rank)
            if best_rank == best_rank_history:
                cnt += 1
                if cnt == 4:
                    break
            else:
                cnt = 0
                best_rank_history = best_rank
        best_idx = rank.index(min(rank))
        return population[best_idx]
