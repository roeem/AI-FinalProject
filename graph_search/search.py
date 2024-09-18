from graph_search import util


class SearchProblem:
    """
    Abstract class outlining the structure of a search problem.

    This class is a template for defining specific search problems. It does not implement any of the methods.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.

        :return: The start state for the search problem.
        :rtype: object
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        Checks if the given state is a valid goal state.

        :param state: The state to check.
        :type state: object
        :return: True if the state is a goal state; False otherwise.
        :rtype: bool
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        Returns a list of successors for the given state.

        For a given state, this method should return a list of triples:
        - `successor`: A successor state.
        - `action`: The action that led to the successor.
        - `stepCost`: The cost of the action.

        :param state: The state to expand.
        :type state: object
        :return: List of triples (successor, action, stepCost).
        :rtype: list[tuple[object, object, float]]
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Performs depth-first search on the given problem.

    This search algorithm explores the deepest nodes in the search tree first. It returns a list of actions
    that leads to the goal. Implements graph search to avoid re-expanding nodes.

    :param problem: The search problem to solve.
    :type problem: SearchProblem
    :return: List of actions to reach the goal state, or None if no solution exists.
    :rtype: list[object] | None
    """
    fringe = util.Stack()
    visited = set()  # set of all the visited states

    start_state = problem.get_start_state()
    fringe.push((start_state, []))

    while not fringe.isEmpty():
        current_state, actions = fringe.pop()

        if problem.is_goal_state(current_state):
            return actions

        elif current_state not in visited:
            visited.add(current_state)

            for successor, action, step_cost in problem.get_successors(current_state):
                fringe.push((successor, actions + [action]))

    return None


class Stage:
    def __init__(self, state, action, total_cost, predecessor):
        self.state = state
        self.action = action
        self.total_cost = total_cost
        self.predecessor = predecessor


def uniform_cost_search(problem):
    """
    Performs uniform cost search on the given problem.

    This search algorithm expands the node with the least total cost first. It returns a list of actions
    that leads to the goal. Implements graph search to avoid re-expanding nodes.

    :param problem: The search problem to solve.
    :type problem: SearchProblem
    :return: List of actions to reach the goal state, or None if no solution exists.
    :rtype: list[object] | None
    """
    fringe = util.PriorityQueue()
    visited = set()  # set of all the visited states

    start_state = problem.get_start_state()
    fringe.push(Stage(start_state, None, 0, None), 0)

    while not fringe.isEmpty():
        stage = fringe.pop()
        current_state, action, total_cost = stage.state, stage.action, stage.total_cost

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.is_goal_state(current_state):
            actions = []
            while stage.predecessor is not None:
                actions.append(stage.action)
                stage = stage.predecessor
            return actions[::-1]

        for successor, action, step_cost in problem.get_successors(current_state):
            current_cost = total_cost + step_cost
            fringe.push(Stage(successor, action, current_cost, stage), current_cost)

    return None


def null_heuristic(state, problem=None):
    """
    A trivial heuristic function that always returns 0.

    This heuristic does not provide any useful information for guiding the search and is used as a default.

    :param state: The current state.
    :type state: object
    :param problem: The search problem instance.
    :type problem: SearchProblem | None
    :return: The heuristic estimate, which is always 0.
    :rtype: float
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Performs A* search on the given problem.

    This search algorithm expands the node with the lowest combined cost and heuristic value first. It returns
    a list of actions that leads to the goal. Implements graph search to avoid re-expanding nodes.

    :param problem: The search problem to solve.
    :type problem: SearchProblem
    :param heuristic: A heuristic function to estimate the cost from the current state to the goal.
    :type heuristic: callable | null_heuristic
    :return: List of actions to reach the goal state, or None if no solution exists.
    :rtype: list[object] | None
    """
    fringe = util.PriorityQueue()
    visited = set()  # set of all the visited states

    start_state = problem.get_start_state()
    start_cost = heuristic(start_state, problem)
    fringe.push(Stage(start_state, None, 0, None), start_cost)

    while not fringe.isEmpty():
        stage = fringe.pop()
        current_state, action, total_cost = stage.state, stage.action, stage.total_cost

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.is_goal_state(current_state):
            actions = []
            while stage.predecessor is not None:
                actions.append(stage.action)
                stage = stage.predecessor
            return actions[::-1]

        for successor, action, step_cost in problem.get_successors(current_state):
            current_cost = total_cost + step_cost
            priority = current_cost + heuristic(successor, problem)
            fringe.push(Stage(successor, action, current_cost, stage), priority)

    return None


# Abbreviations for convenience
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
