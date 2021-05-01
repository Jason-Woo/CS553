import numpy as np


class GeneticAlg(object):
    def __init__(self, idx, candidates, neighbor):
        self.population_size = 100
        self.mutation_rate = 0.01
        self.max_iter = 1000
        self.index = idx
        self.candidates = candidates
        self.neighbor = neighbor

    def scoring(self, weight):
        print('Scoring...')
        avg_rank = []
        for i in range(len(weight)):
            if i % 100 == 0:
                print(i, '/', len(weight))
            tmp_rank = 0
            curr_weight = weight[i]
            score = np.dot(self.index, curr_weight)
            score_sorted_idx = np.argsort(-score)
            for j, c in enumerate(self.candidates):
                if c in self.neighbor:
                    tmp_rank += score_sorted_idx[j]
            tmp_rank /= len(self.neighbor)
            avg_rank.append(tmp_rank)
        return avg_rank

    def keep_fittest(self, rank, population):
        rank_cpy = rank[:]
        population_fittest = []
        for _ in range(self.population_size):
            curr_min = rank_cpy.index(min(rank_cpy))
            population_fittest.append(population[curr_min])
            rank_cpy[curr_min] = 99999999
        return np.array(population_fittest)

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
        # print(population)
        # print('------------')
        # print(new_population)
        # print('------------')
        # print(np.concatenate((population, new_population)))
        return np.concatenate((population, new_population))

    def run(self):
        population = np.random.randint(0, 256, (self.population_size, 4))
        rank = self.scoring(population)

        best_rank = min(rank)
        cnt = 0
        best_rank_history = best_rank

        for _ in range(self.max_iter):
            print("Average Rank ", best_rank)
            population = self.next_genration(population)

            rank = self.scoring(population)
            population = self.keep_fittest(rank, population)

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
