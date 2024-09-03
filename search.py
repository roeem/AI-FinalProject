"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
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


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
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
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
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
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
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
                # TODO remove from here
                if not (0 <= heuristic(stage.predecessor.state, problem) <= heuristic(stage.state, problem) + (stage.total_cost - stage.predecessor.total_cost)):
                    res = heuristic(stage.predecessor.state, problem) - (heuristic(stage.state, problem) + (stage.total_cost - stage.predecessor.total_cost))
                    if res > 0.001:
                        print(f"Heuristic not consistent - {res}")
                # TODO: remove until here
                actions.append(stage.action)
                stage = stage.predecessor
            return actions[::-1]

        for successor, action, step_cost in problem.get_successors(current_state):
            current_cost = total_cost + step_cost
            priority = current_cost + heuristic(successor, problem)
            fringe.push(Stage(successor, action, current_cost, stage), priority)

    return None


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
