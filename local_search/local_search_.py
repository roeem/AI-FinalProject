import collections
import math
import random
from threading import Thread
from typing import Callable, Any
from abc import ABC
from local_search.thread_safe_set import TSS
import numpy as np


class LocalSearchProblem(ABC):
    """
    Abstract base class for a local search problem.

    This class defines the structure of a local search problem but does not implement
    any of the methods. Subclasses should implement the following methods:
    - get_initial_state
    - get_neighbors
    - fitness
    """

    def get_initial_state(self) -> Any:
        """
        Returns the start state for the search problem.
        """
        pass

    def get_neighbors(self, state: Any) -> list[Any]:
        """
        For a given state, returns a list of neighboring states.

        :param state: The current state in the search problem.
        :type state: Any
        :return: List of neighboring states.
        :rtype: list[Any]
        """
        pass

    def fitness(self, state: Any) -> float:
        """
        Returns the fitness of a given state.

        :param state: The state to evaluate.
        :type state: Any
        :return: The fitness value of the state.
        :rtype: float
        """
        pass


# region Hill Climbing
def hill_climbing(problem: LocalSearchProblem, max_iter=10 ** 5):
    """
    Implements the Hill Climbing algorithm.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param max_iter: Maximum number of iterations.
    :type max_iter: int
    :return: A state that is a local maximum.
    :rtype: Any
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
                        eps=1e-25):
    """
    Implements the Simulated Annealing algorithm.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param schedule: A function that computes the temperature based on the current iteration.
    :type schedule: Callable[[int], float]
    :param max_iter: Maximum number of iterations.
    :type max_iter: int
    :param eps: A small value to determine when to stop the algorithm.
    :type eps: float
    :return: A state that is a local maximum.
    :rtype: Any
    """
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


def exp_cool_schedule(t: int, T0=100000, alpha=0.95) -> float:
    """
    Exponential cooling schedule for simulated annealing.

    :param t: Current iteration.
    :type t: int
    :param T0: Initial temperature.
    :type T0: float
    :param alpha: Cooling rate.
    :type alpha: float
    :return: Temperature at iteration t.
    :rtype: float
    """
    return T0 * (alpha ** t)


def linear_cool_schedule(t: int, T0=10000, rate=1) -> float:
    """
    Linear cooling schedule for simulated annealing.

    :param t: Current iteration.
    :type t: int
    :param T0: Initial temperature.
    :type T0: float
    :param rate: Rate of temperature decrease.
    :type rate: float
    :return: Temperature at iteration t.
    :rtype: float
    """
    return T0 - t * rate


def log_cool_schedule(t: int, T0=100, beta=5) -> float:
    """
    Logarithmic cooling schedule for simulated annealing.

    :param t: Current iteration.
    :type t: int
    :param T0: Initial temperature.
    :type T0: float
    :param beta: Logarithmic rate.
    :type beta: float
    :return: Temperature at iteration t.
    :rtype: float
    """
    return T0 / (1 + beta * math.log(1 + t))


# endregion

# region Stochastic Beam Search - specific to DegreePlanningProblem
def single_beam_search(problem: LocalSearchProblem, state, all_neighbors: TSS):
    """
    Adds neighbors of the given state to a thread-safe set.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param state: The state to generate neighbors for.
    :type state: Any
    :param all_neighbors: Thread-safe set to collect neighbors.
    :type all_neighbors: TSS
    """
    for neighbor in problem.get_neighbors(state):
        all_neighbors.add(neighbor)


def stochastic_beam_search(problem: LocalSearchProblem, k: int = 50, T: float = 1, max_iter=10 ** 5):
    """
    Implements the Stochastic Beam Search algorithm.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param k: Number of initial states and number of neighbors to sample.
    :type k: int
    :param T: Temperature parameter for softmax sampling.
    :type T: float
    :param max_iter: Maximum number of iterations.
    :type max_iter: int
    :return: The best state found after max_iter iterations.
    :rtype: Any
    """
    init_states = {problem.get_initial_state() for _ in range(k)}
    best_state = max(init_states, key=problem.fitness)
    all_neighbors: TSS = TSS()
    # first iteration
    threads = create_threads(problem, init_states, all_neighbors)
    # we want to keep the results from last l iters
    last_best: collections.deque[float] = collections.deque(maxlen=10)
    for _ in range(max_iter):
        wait_for_all_threads(threads)
        k_neighbors = sample_k_neighbors(problem, all_neighbors, k, T)
        best_state = max(k_neighbors, key=problem.fitness)
        last_best.append(problem.fitness(best_state))
        if stop_condition(last_best):
            return best_state
        all_neighbors: TSS = TSS()
        threads = create_threads(problem, k_neighbors, all_neighbors)
    print("******* Reached max_iterations ! *******\n")
    return best_state


def sample_k_neighbors(problem: LocalSearchProblem, all_neighbors: TSS, k: int, T: float) -> set:
    """
    Samples k neighbors based on their scores using softmax probabilities.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param all_neighbors: Thread-safe set of all neighbors.
    :type all_neighbors: TSS
    :param k: Number of neighbors to sample.
    :type k: int
    :param T: Temperature parameter for softmax sampling.
    :type T: float
    :return: Set of sampled neighbors.
    :rtype: set
    """
    all_neighbors = list(all_neighbors)
    scores = [problem.fitness(neighbor) for neighbor in all_neighbors]
    probabilities = softmax(scores, T)

    # Sample k indices based on the computed probabilities
    indices = np.arange(len(scores))
    chosen_indices = np.random.choice(indices, size=k, p=probabilities, replace=False)
    return {all_neighbors[i] for i in chosen_indices}


def stop_condition(last_best: collections.deque[float]) -> bool:
    """
    Determines whether to stop the search based on the improvement of the best state.

    :param last_best: Recent fitness values of the best states.
    :type last_best: collections.deque
    :return: True if the search should stop, otherwise False.
    :rtype: bool
    """
    eps = 1e-3
    if len(last_best) == last_best.maxlen:
        return max(last_best) - min(last_best) <= eps
    return False


def wait_for_all_threads(threads: list[Thread]):
    """
    Waits for all threads to finish.

    :param threads: List of threads to wait for.
    :type threads: list[Thread]
    """
    for thread in threads:
        thread.join()


def softmax(scores: list[float], T: float):
    """
    Computes softmax probabilities from scores with temperature scaling.

    :param scores: List of scores to normalize.
    :type scores: list[float]
    :param T: Temperature parameter.
    :type T: float
    :return: Softmax probabilities.
    :rtype: np.ndarray
    """
    scores = np.array(scores) / T
    exp_scores = np.exp(scores - np.max(scores))  # Numerical stability
    return exp_scores / exp_scores.sum()


def create_threads(problem: LocalSearchProblem, states: set, all_neighbors: TSS) -> list[Thread]:
    """
    Creates and starts threads for generating neighbors.

    :param problem: A LocalSearchProblem object.
    :type problem: LocalSearchProblem
    :param states: Set of states to generate neighbors for.
    :type states: set
    :param all_neighbors: Thread-safe set to collect neighbors.
    :type all_neighbors: TSS
    :return: List of created threads.
    :rtype: list[Thread]
    """
    threads = []
    for state in states:
        thread = Thread(target=single_beam_search, args=(problem, state, all_neighbors))
        threads.append(thread)
        thread.start()
    return threads


# endregion

# Abbreviations
hill = hill_climbing
sa = simulated_annealing
beam = stochastic_beam_search
