"""
In local_search.py, you will implement generic search algorithms
"""
import math
import random
from typing import Callable

import util


class LocalSearchProblem:
    """
    This class outlines the structure of a local search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_initial_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def get_neighbors(self, state):
        """
        state: Search state

        For a given state, this should return a list of states.
        """
        util.raiseNotDefined()

    def fitness(self, state):
        """
        Returns the fitness of a state
        """
        util.raiseNotDefined()


def hill_climbing(problem: LocalSearchProblem, max_iter=10 ** 5):
    """
    This function should implement the Hill Climbing algorithm

    :param problem: a LocalSearchProblem object
    :return: a state that is a local maximum
    """
    current = problem.get_initial_state()
    for _ in range(max_iter):
        neighbors = problem.get_neighbors(current)
        best_neighbor_val = problem.fitness(max(neighbors, key=problem.fitness))
        best_neighbors = [n for n in neighbors if problem.fitness(n) == best_neighbor_val]
        if best_neighbor_val <= problem.fitness(current):
            return current
        current = random.choice(best_neighbors)

    print("******* Reached max_iterations ! *******\n" * 100)
    return current


def simulated_annealing(problem: LocalSearchProblem, schedule: Callable[[int], float], max_iter=10 ** 5, eps=1e-10):
    current = problem.get_initial_state()
    for t in range(max_iter):
        T = schedule(t)
        if T < eps:
            return current
        neighbor = random.choice(problem.get_neighbors(current))
        delta = problem.fitness(neighbor) - problem.fitness(current)
        if delta > 0:
            current = neighbor
        elif random.random() < math.e ** (delta / T):
            current = neighbor
    print("******* Reached max_iterations ! *******\n" * 100)
    return current


def exp_cool_schedule(t: int, T0=10000, alpha=0.9) -> float:
    return T0 * (alpha ** t)

def linear_cool_schedule(t: int, T0=1000, rate=1) -> float:
    #If we choose rate = T0/max_iter- we'll use all the iterations.
    return T0 - t * rate


def log_cool_schedule(t: int, T0=100, beta=2) -> float:
    return T0 / (1 + beta * math.log(1 + t))
