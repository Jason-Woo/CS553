from genetic_alg import *
import numpy as np

index = np.loadtxt('tmp.csv', delimiter=",")
candidates = np.loadtxt('tmp1.csv', delimiter=",", dtype=int)
adj = np.loadtxt('tmp2.csv', delimiter=",", dtype=int)

# index = index * 100

print(index)
print(candidates)
print(adj)

genetic = GeneticAlg(index, candidates, adj)

weight = genetic.run()
score = np.dot(index, weight)
score_list = score.tolist()
recomm_list = []
while len(recomm_list) < 15:
    best_idx = score_list.index(min(score_list))
    if candidates[best_idx] not in adj:
        recomm_list.append(candidates[best_idx])
        score_list[best_idx] = 9999999999
print(recomm_list)