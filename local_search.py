"""
In local_search.py, you will implement generic search algorithms
"""
import math
import random
from threading import Thread
from typing import Callable, Any
from abc import ABC
import numpy as np

from thread_safe_set import TsSet


class LocalSearchProblem(ABC):
    """
    This class outlines the structure of a local search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_initial_state(self) -> Any:
        """
        Returns the start state for the search problem
        """
        pass

    def get_neighbors(self, state: Any) -> list[Any]:
        """
        state: Search state

        For a given state, this should return a list of states.
        """
        pass

    def fitness(self, state: Any) -> float:
        """
        Returns the fitness of a state
        """
        pass


# region Hill Climbing
def hill_climbing(problem: LocalSearchProblem, max_iter=10 ** 5):
    """
    This function should implement the Hill Climbing algorithm

    :param problem: a LocalSearchProblem object
    :param max_iter: maximum of iterations
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

    print("******* Reached max_iterations ! *******\n")
    return current


# endregion

# region Simulated Annealing
def simulated_annealing(problem: LocalSearchProblem, schedule: Callable[[int], float], max_iter=10 ** 5,
                        eps=1e-10):
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
    print("******* Reached max_iterations ! *******\n")
    return current


def exp_cool_schedule(t: int, T0=10000, alpha=0.9) -> float:
    return T0 * (alpha ** t)


def linear_cool_schedule(t: int, T0=1000, rate=1) -> float:
    # If we choose rate = T0/max_iter- we'll use all the iterations.
    return T0 - t * rate


def log_cool_schedule(t: int, T0=100, beta=5) -> float:
    return T0 / (1 + beta * math.log(1 + t))


# endregion

# region Stochastic Beam Search - specific to DegreePlanningProblem
def single_beam_search(problem: LocalSearchProblem, state, all_neighbors: TsSet):
    for neighbor in problem.get_neighbors(state):
        all_neighbors.add(neighbor)


def wait_for_all_threads(threads: list[Thread]):
    for thread in threads:
        thread.join()


def softmax(scores: list[float], T: float) -> np.ndarray[float]:
    """Compute softmax probabilities from scores with temperature scaling."""
    scores = np.array(scores) / T
    exp_scores = np.exp(scores - np.max(scores))  # Numerical stability TODO: check the "- np.max(scores)"
    return exp_scores / exp_scores.sum()


def sample_k_neighbors(problem: LocalSearchProblem, all_neighbors: TsSet, k: int, T: float) -> set:
    """Sample k neighbors based on their scores using softmax probabilities."""
    all_neighbors = list(all_neighbors)
    scores = [problem.fitness(neighbor) for neighbor in all_neighbors]
    probabilities = softmax(scores, T)

    # Sample k indices based on the computed probabilities
    indices = np.arange(len(scores))
    chosen_indices = np.random.choice(indices, size=k, p=probabilities, replace=False)
    return {all_neighbors[i] for i in chosen_indices}


def stop_condition(problem: LocalSearchProblem, state) -> bool:
    ############ for Roee ###############
    from degree_plan import DegreePlan
    from local_degree_planning_problem import DegreePlanningProblem
    if isinstance(problem, DegreePlanningProblem):
        problem: DegreePlanningProblem = problem
    if isinstance(state, DegreePlan):
        state: DegreePlan = state
    #####################################

    eps = 0.5  # todo: check this
    return (state.total_points == problem.target_points and
            state.mandatory_points == problem.mandatory_points and
            problem.get_upper_bound() - state.avg_grade <= eps)


def create_threads(problem: LocalSearchProblem, states: set, all_neighbors: TsSet) -> list[Thread]:
    threads = []
    for state in states:
        thread = Thread(target=single_beam_search, args=(problem, state, all_neighbors))
        thread.start()
        threads.append(thread)
    return threads


def stochastic_beam_search(problem: LocalSearchProblem, k: int = 10, T: float = 1, max_iter=10 ** 5):
    init_states = {problem.get_initial_state() for _ in range(k)}
    best_state = max(init_states, key=problem.fitness)
    all_neighbors: TsSet = TsSet()
    # first iteration
    threads = create_threads(problem, init_states, all_neighbors)

    for _ in range(max_iter):
        wait_for_all_threads(threads)
        k_neighbors = sample_k_neighbors(problem, all_neighbors, k, T)
        cur_best_state = max(k_neighbors, key=problem.fitness)
        best_state = max(best_state, cur_best_state, key=problem.fitness)
        if stop_condition(problem, best_state):
            return best_state  # todo: return the best
        all_neighbors: TsSet = TsSet()
        threads = create_threads(problem, k_neighbors, all_neighbors)
    print("******* Reached max_iterations ! *******\n")
    return best_state

# endregion
