class Model(object):
    def __init__(self):
        self.target = -1
        self.candidates = []
        self.adjacency_list = []
        self.checkin_usr_list = []
        self.checkin_time_list = []
        self.check_loc_list = []
        self.weight = [-1] * 3


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
        return 1

    def get_idx(self):
        index = []
        for i in self.candidates:
            tmp_idx = [self.adjacent_nodes(i), self.density_ints(i), self.density_union(i), self.mobility_similarity(i)]
            index.append(tmp_idx)
        return index

    def genetic_alg(self):
        # TODO
        return 0
