"""
In local_search.py, you will implement generic search algorithms
"""
import random

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


def hill_climbing(problem: LocalSearchProblem, max_iter=10**5):
    """
    This function should implement the Hill Climbing algorithm

    :param problem: a LocalSearchProblem object
    :return: a state that is a local maximum
    """
    current = problem.get_initial_state()
    while True or max_iter > 0:
        neighbors = problem.get_neighbors(current)
        best_neighbor_val = problem.fitness(max(neighbors, key=problem.fitness))
        best_neighbors = [n for n in neighbors if problem.fitness(n) == best_neighbor_val]
        best_neighbor = random.choice(best_neighbors)
        if problem.fitness(best_neighbor) <= problem.fitness(current):
            return current
        current = best_neighbor
        max_iter -= 1
    return current


