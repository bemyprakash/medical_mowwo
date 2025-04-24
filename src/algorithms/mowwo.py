import numpy as np
import random

class MOWWO:
    def __init__(self, population_size, max_iterations, objectives, problem, constraints, KN=5, hmax=10):
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.objectives = objectives
        self.problem = problem
        self.constraints = constraints
        self.KN = KN
        self.hmax = hmax
        self.population = self.initialize_population()
        self.stagnation = [0] * self.population_size

    def initialize_population(self):
        pop = []
        for _ in range(self.population_size):
            sol = self.random_solution()
            pop.append(sol)
        return pop

    def random_solution(self):
        # Section 4.1: Random but feasible-like solution
        m, n, K, K1 = self.problem.m, self.problem.n, self.problem.K, self.problem.K1
        xijk = np.random.randint(0, 3, size=(m, n, K1))
        xjjk = np.random.randint(0, 3, size=(n, n, K1))
        yo = np.random.randint(0, 3, size=(m, n))
        ys = np.random.randint(0, 3, size=(m, n))
        ym = np.random.randint(0, 3, size=(m, n))
        yv = np.random.randint(0, 3, size=(m, n))
        return {'xijk': xijk, 'xjjk': xjjk, 'yo': yo, 'ys': ys, 'ym': ym, 'yv': yv}

    def evaluate_population(self, population):
        evaluated = []
        for sol in population:
            obj1, obj2 = self.problem.evaluate(sol['xijk'], sol['xjjk'], sol['yo'], sol['ys'], sol['ym'], sol['yv'])
            feasible = self.is_feasible(sol)
            evaluated.append({'solution': sol, 'objectives': (obj1, obj2), 'feasible': feasible})
        return evaluated

    def is_feasible(self, sol):
        # Placeholder: always returns True. Replace with real constraint checks.
        return True

    def non_dominated_sorting(self, evaluated):
        # NSGA-II style non-dominated sorting
        population_size = len(evaluated)
        S = [[] for _ in range(population_size)]
        n = [0 for _ in range(population_size)]
        rank = [0 for _ in range(population_size)]
        fronts = [[]]
        for p in range(population_size):
            S[p] = []
            n[p] = 0
            for q in range(population_size):
                if self.dominates(evaluated[p], evaluated[q]):
                    S[p].append(q)
                elif self.dominates(evaluated[q], evaluated[p]):
                    n[p] += 1
            if n[p] == 0:
                rank[p] = 0
                fronts[0].append(p)
        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in S[p]:
                    n[q] -= 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        return rank, fronts

    def dominates(self, ind1, ind2):
        # Feasible dominates infeasible
        if ind1['feasible'] and not ind2['feasible']:
            return True
        if not ind1['feasible'] and ind2['feasible']:
            return False
        # Both feasible or both infeasible: Pareto dominance (maximization)
        better_or_equal = all(a >= b for a, b in zip(ind1['objectives'], ind2['objectives']))
        strictly_better = any(a > b for a, b in zip(ind1['objectives'], ind2['objectives']))
        return better_or_equal and strictly_better

    def wavelength(self, rank, rankmax):
        # Equation (31): wavelength = rank / rankmax
        return rank / rankmax if rankmax > 0 else 1.0

    def mutate_wave(self, sol, wavelength):
        # Mutate solution in a "wave" radius proportional to wavelength
        new_sol = {k: np.copy(v) for k, v in sol.items()}
        for key, arr in new_sol.items():
            if np.random.rand() < wavelength:
                idx = tuple(np.random.randint(0, s) for s in arr.shape)
                arr[idx] = max(0, arr[idx] + random.choice([-1, 1]))
        return new_sol

    def repair(self, sol):
        # Placeholder: add real repair logic for constraints
        return sol

    def local_search(self, sol):
        # Generate KN neighbors by small perturbations
        neighbors = []
        for _ in range(self.KN):
            neighbor = self.mutate_wave(sol, 0.1)
            neighbors.append(self.repair(neighbor))
        return neighbors

    def run(self):
        population = self.population
        stagnation = [0] * self.population_size
        best_front = []
        for iteration in range(self.max_iterations):
            evaluated = self.evaluate_population(population)
            rank, fronts = self.non_dominated_sorting(evaluated)
            rankmax = max(rank)
            # Generate children
            children = []
            for idx, ind in enumerate(evaluated):
                wl = self.wavelength(rank[idx], rankmax)
                child = self.mutate_wave(ind['solution'], wl)
                child = self.repair(child)
                children.append(child)
            # Evaluate children
            evaluated_children = self.evaluate_population(children)
            # Replacement: if child better than parent, replace
            new_population = []
            for i in range(self.population_size):
                if self.dominates(evaluated_children[i], evaluated[i]):
                    new_population.append(children[i])
                    stagnation[i] = 0
                else:
                    new_population.append(population[i])
                    stagnation[i] += 1
            # Local search if new best found
            nd_indices = fronts[0]
            if nd_indices and (best_front == [] or len(nd_indices) < len(best_front)):
                best_front = nd_indices
                for idx in nd_indices:
                    neighbors = self.local_search(evaluated[idx]['solution'])
                    for neighbor in neighbors:
                        new_population.append(neighbor)
            # Stagnation: reinitialize if needed
            for i in range(self.population_size):
                if stagnation[i] > self.hmax:
                    new_population[i] = self.random_solution()
                    stagnation[i] = 0
            # Truncate to population size
            population = new_population[:self.population_size]
        # Final non-dominated sorting
        evaluated = self.evaluate_population(population)
        rank, fronts = self.non_dominated_sorting(evaluated)
        nd_solutions = [evaluated[i]['solution'] for i in fronts[0]]
        return nd_solutions